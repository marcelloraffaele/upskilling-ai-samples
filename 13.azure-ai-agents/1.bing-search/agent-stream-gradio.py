import os, sys,json, re
from typing import Optional,Any, List, Dict
from azure.ai.projects import AIProjectClient
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import BingGroundingTool, MessageRole, ThreadMessage, ToolSet, ThreadRun, RunStep, RunStepDeltaChunk, MessageDeltaChunk, AgentStreamEvent, AgentEventHandler,MessageTextContent
import gradio as gr
from gradio import ChatMessage

from dotenv import load_dotenv
load_dotenv()

class LoggingToolSet(ToolSet):

    def __init__(self):
        super().__init__()
        print("Initialized LoggingToolSet")

    def execute_tool_calls(self, tool_calls: List[Any]) -> List[dict]:
        """
        Execute the upstream calls, printing only two lines per function:
        1) The function name + its input arguments
        2) The function name + its output result
        """

        print("***********************************************************************Tool calls:")

        # For each function call, print the input arguments
        for c in tool_calls:
            if hasattr(c, "function") and c.function:
                fn_name = c.function.name
                fn_args = c.function.arguments
                print(f"{fn_name} inputs > {fn_args} (id:{c.id})")

        # Execute the tool calls (superclass logic)
        raw_outputs = super().execute_tool_calls(tool_calls)

        # Print the output of each function call
        for item in raw_outputs:
            print(f"output > {item['output']}")

        return raw_outputs
    
    async def execute_tool_calls(self, tool_calls: List[Any]) -> Any:
        """
        Execute a tool of the specified type with the provided tool calls concurrently.

        :param List[Any] tool_calls: A list of tool calls to execute.
        :return: The output of the tool operations.
        :rtype: Any
        """
        print("*********************************************************async Tool calls:")

        raw_outputs = super().execute_tool_calls(tool_calls)

        return raw_outputs

def extract_bing_query(request_url: str) -> str:
    """
    Extract the query string from something like:
      https://api.bing.microsoft.com/v7.0/search?q="latest news about Microsoft January 2025"
    Returns: latest news about Microsoft January 2025
    """
    match = re.search(r'q="([^"]+)"', request_url)
    if match:
        return match.group(1)
    # If no match, fall back to entire request_url
    return request_url

def convert_dict_to_chatmessage(msg: dict) -> ChatMessage:
    """
    Convert a legacy dict-based message to a gr.ChatMessage.
    Uses the 'metadata' sub-dict if present.
    """
    return ChatMessage(
        role=msg["role"],
        content=msg["content"],
        metadata=msg.get("metadata", None)
    )

def azure_enterprise_chat(user_message: str, history: List[dict]):

    """
    Accumulates partial function arguments into ChatMessage['content'], sets the
    corresponding tool bubble status from "pending" to "done" on completion,
    and also handles non-function calls like bing_grounding or file_search by appending a
    "pending" bubble. Then it moves them to "done" once tool calls complete.

    This function returns a list of ChatMessage objects directly (no dict conversion).
    Your Gradio Chatbot should be type="messages" to handle them properly.
    """

    # Convert existing history from dict to ChatMessage
    conversation = []
    for msg_dict in history:
        conversation.append(convert_dict_to_chatmessage(msg_dict))

    # Append the user's new message
    conversation.append(ChatMessage(role="user", content=user_message))

    # Immediately yield two outputs to clear the textbox
    yield conversation, ""

    # Mappings for partial function calls
    call_id_for_index: Dict[int, str] = {}
    partial_calls_by_index: Dict[int, dict] = {}
    partial_calls_by_id: Dict[str, dict] = {}
    in_progress_tools: Dict[str, ChatMessage] = {}

    # Titles for tool bubbles
    function_titles = {
        "fetch_weather": "☁️ fetching weather",
        "fetch_datetime": "🕒 fetching datetime",
        "fetch_stock_price": "📈 fetching financial info",
        "send_email": "✉️ sending mail",
        "file_search": "📄 searching docs",
        "bing_grounding": "🔍 searching bing",
    }

    def get_function_title(fn_name: str) -> str:
        return function_titles.get(fn_name, f"🛠 calling {fn_name}")
    
    def accumulate_args(storage: dict, name_chunk: str, arg_chunk: str):
        """Accumulates partial JSON data for a function call."""
        if name_chunk:
            storage["name"] += name_chunk
        if arg_chunk:
            storage["args"] += arg_chunk

    def finalize_tool_call(call_id: str):
        """Creates or updates the ChatMessage bubble for a function call."""
        if call_id not in partial_calls_by_id:
            return
        data = partial_calls_by_id[call_id]
        fn_name = data["name"].strip()
        fn_args = data["args"].strip()
        if not fn_name:
            return

        if call_id not in in_progress_tools:
            # Create a new bubble with status="pending"
            msg_obj = ChatMessage(
                role="assistant",
                content=fn_args or "",
                metadata={
                    "title": get_function_title(fn_name),
                    "status": "pending",
                    "id": f"tool-{call_id}"
                }
            )
            conversation.append(msg_obj)
            in_progress_tools[call_id] = msg_obj
        else:
            # Update existing bubble
            msg_obj = in_progress_tools[call_id]
            msg_obj.content = fn_args or ""
            msg_obj.metadata["title"] = get_function_title(fn_name)

    def complete_tool_call(tcall: dict):
        """Updates the ChatMessage bubble for a function call."""
        t_type = tcall.get("type", "")
        call_id = tcall.get("id")
        #print(f"[complete_tool_call] call_id {call_id}")

        if t_type == "bing_grounding":
            bing_grounding = tcall.get("bing_grounding")
            request_url = bing_grounding.get("requesturl", "") 
            query_str = extract_bing_query(request_url)
            for cm in conversation:
                if cm.role != "user" and cm.content == query_str:
                    print(f"[complete_tool_call] found cm {cm}")
                    # Update existing bubble
                    cm.metadata["status"] = "done"
                    break

        else:
            for cm in conversation:
                print(f"[complete_tool_call] cm={cm}")
                if cm.role != "user" and cm.metadata["id"] == f"tool-{call_id}":
                    print(f"[complete_tool_call] found cm {cm}")
                    # Update existing bubble
                    cm.metadata["status"] = "done"

    def upsert_tool_call(tcall: dict):
        """
        1) Check the call type
        2) If "function", gather partial name/args
        3) If "bing_grounding" or "file_search", show a pending bubble
        """
        t_type = tcall.get("type", "")
        call_id = tcall.get("id")

        # --- BING GROUNDING ---
        if t_type == "bing_grounding":
            request_url = tcall.get("bing_grounding", {}).get("requesturl", "")
            if not request_url.strip():
                return

            query_str = extract_bing_query(request_url)
            if not query_str.strip():
                return

            msg_obj = ChatMessage(
                role="assistant",
                content=query_str,
                metadata={
                    "title": get_function_title("bing_grounding"),
                    "status": "pending",
                    "id": f"tool-{call_id}" if call_id else "tool-noid"
                }
            )
            conversation.append(msg_obj)
            if call_id:
                in_progress_tools[call_id] = msg_obj
            return

        # --- FILE SEARCH ---
        elif t_type == "file_search":
            msg_obj = ChatMessage(
                role="assistant",
                content="searching docs...",
                metadata={
                    "title": get_function_title("file_search"),
                    "status": "pending",
                    "id": f"tool-{call_id}" if call_id else "tool-noid"
                }
            )
            conversation.append(msg_obj)
            if call_id:
                in_progress_tools[call_id] = msg_obj
            return

        # --- NON-FUNCTION CALLS ---
        elif t_type != "function":
            return

        # --- FUNCTION CALL PARTIAL-ARGS ---
        index = tcall.get("index")
        new_call_id = call_id
        fn_data = tcall.get("function", {})
        name_chunk = fn_data.get("name", "")
        arg_chunk = fn_data.get("arguments", "")

        if new_call_id:
            call_id_for_index[index] = new_call_id

        call_id = call_id_for_index.get(index)
        if not call_id:
            # Accumulate partial
            if index not in partial_calls_by_index:
                partial_calls_by_index[index] = {"name": "", "args": ""}
            accumulate_args(partial_calls_by_index[index], name_chunk, arg_chunk)
            return

        if call_id not in partial_calls_by_id:
            partial_calls_by_id[call_id] = {"name": "", "args": ""}

        if index in partial_calls_by_index:
            old_data = partial_calls_by_index.pop(index)
            partial_calls_by_id[call_id]["name"] += old_data.get("name", "")
            partial_calls_by_id[call_id]["args"] += old_data.get("args", "")

        # Accumulate partial
        accumulate_args(partial_calls_by_id[call_id], name_chunk, arg_chunk)

        # Create/update the function bubble
        finalize_tool_call(call_id)

    # Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
    # You need to login to Azure subscription via Azure CLI and set the environment variables
    project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

    # Create an AIProjectClient instance
    project_client = AIProjectClient(
        endpoint=project_endpoint,
        credential=DefaultAzureCredential()  # Use Azure Default Credential for authentication
    )

    #conn_id = os.environ["BING_CONNECTION_NAME"]  # Ensure the BING_CONNECTION_NAME environment variable is set
    conn_id = project_client.connections.get(name=os.environ["BING_RESOURCE_NAME"]).id

    # Initialize the Bing Grounding tool
    bing_tool = BingGroundingTool(connection_id=conn_id)

    toolset = LoggingToolSet()
    toolset.add(bing_tool)

    #for tool in toolset._tools:
    #    tool_name = tool.__class__.__name__
    #    print(f"tool > {tool_name}")
    #    for definition in tool.definitions:
    #        if hasattr(definition, "function"):
    #            fn = definition.function
    #            print(f"{fn.name} > {fn.description}")
    #        else:
    #            pass

    with project_client:

        with project_client.agents as agents_client:

            # Create an agent with the Bing Grounding tool
            agent = agents_client.create_agent(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
                name="my-agent",  # Name of the agent
                instructions="You are a helpful agent.",  # Instructions for the agent
                toolset=toolset,  # Attach the Bing Grounding tool
            )
            # [END create_agent_with_deep_research_tool]
            print(f"Created agent, ID: {agent.id}")

            # Create thread for communication
            thread = agents_client.threads.create()
            print(f"Created thread, ID: {thread.id}")

            # Recreate the thread history from the conversation
            for msg in conversation:
                
                agents_client.messages.create(
                    thread_id=thread.id,
                    role=msg.role,
                    content=msg.content,
                )
            print("Recreated thread history")

            
            with agents_client.runs.stream(thread_id=thread.id, agent_id=agent.id) as stream:
                for event_type, event_data, func_return in stream:
                    # Debug print of all events
                    #if not isinstance(event_data, MessageDeltaChunk):
                    #    #print(f"\n[Generic] event_type={event_type} dump={json.dumps(event_data.as_dict(), indent=2)}") 
                    #    print(f">> {json.dumps(event_data.as_dict())}")

                    if event_type == "thread.run.step.delta":
                        step_delta = event_data.get("delta", {}).get("step_details", {})
                        if step_delta.get("type") == "tool_calls":
                            for tcall in step_delta.get("tool_calls", []):
                                upsert_tool_call(tcall)

                    elif event_type == "thread.run.step.completed":
                        print(f"\n[thread.run.step.completed] dump={json.dumps(event_data.as_dict())}")
                        #print(f"[thread.run.step.completed] in_progress_tools dump={json.dumps(in_progress_tools)}")
                        step_type = event_data["type"]
                        if step_type == "tool_calls":
                            for tcall in event_data["step_details"].get("tool_calls", []):
                                complete_tool_call(tcall)
                            yield conversation, ""


                    # 2) run_step
                    elif event_type == "run_step":
                        step_type = event_data["type"]
                        step_status = event_data["status"]

                        # If tool calls are in progress, new or partial
                        if step_type == "tool_calls" and step_status == "in_progress":
                            for tcall in event_data["step_details"].get("tool_calls", []):
                                upsert_tool_call(tcall)
                            yield conversation, ""

                        elif step_type == "tool_calls" and step_status == "completed":
                            print(f"[run_step] tool_calls completed")
                            for cid, msg_obj in in_progress_tools.items():
                                msg_obj.metadata["status"] = "done"
                            
                            in_progress_tools.clear()
                            partial_calls_by_id.clear()
                            partial_calls_by_index.clear()
                            call_id_for_index.clear()
                            
                            yield conversation, ""

                        elif step_type == "message_creation" and step_status == "in_progress":
                            msg_id = event_data["step_details"]["message_creation"].get("message_id")
                            if msg_id:
                                conversation.append(ChatMessage(role="assistant", content=""))
                            yield conversation, ""

                        elif step_type == "message_creation" and step_status == "completed":
                            yield conversation, ""

                    # 3) partial text from the assistant
                    elif event_type == "thread.message.delta":
                        agent_msg = ""
                        for chunk in event_data["delta"]["content"]:
                            agent_msg += chunk["text"].get("value", "")

                        message_id = event_data["id"]

                        # Try to find a matching assistant bubble
                        matching_msg = None
                        for msg in reversed(conversation):
                            if msg.metadata and msg.metadata.get("id") == message_id and msg.role == "assistant":
                                matching_msg = msg
                                break

                        if matching_msg:
                            # Append newly streamed text
                            matching_msg.content += agent_msg
                        else:
                            # Append to last assistant or create new
                            if (
                                not conversation
                                or conversation[-1].role != "assistant"
                                or (
                                    conversation[-1].metadata
                                    and str(conversation[-1].metadata.get("id", "")).startswith("tool-")
                                )
                            ):
                                conversation.append(ChatMessage(role="assistant", content=agent_msg))
                            else:
                                conversation[-1].content += agent_msg

                        yield conversation, ""

                    # 4) If entire assistant message is completed
                    elif event_type == "thread.message":
                        if event_data["role"] == "assistant" and event_data["status"] == "completed":
                            for cid, msg_obj in in_progress_tools.items():
                                msg_obj.metadata["status"] = "done"
                            in_progress_tools.clear()
                            partial_calls_by_id.clear()
                            partial_calls_by_index.clear()
                            call_id_for_index.clear()
                            yield conversation, ""

                    # 5) Final done
                    elif event_type == "thread.message.completed":
                        for cid, msg_obj in in_progress_tools.items():
                            msg_obj.metadata["status"] = "done"
                        in_progress_tools.clear()
                        partial_calls_by_id.clear()
                        partial_calls_by_index.clear()
                        call_id_for_index.clear()
                        yield conversation, ""
                        break

            # Clean-up and delete the agent once the run is finished.
            # NOTE: Comment out this line if you plan to reuse the agent later.
            agents_client.delete_agent(agent.id)
            print("Deleted agent")
    return conversation, ""

brand_theme = gr.themes.Default(
    primary_hue="blue",
    secondary_hue="blue",
    neutral_hue="gray",
    font=["Segoe UI", "Arial", "sans-serif"],
    font_mono=["Courier New", "monospace"],
    text_size="lg",
).set(
    button_primary_background_fill="#0f6cbd",
    button_primary_background_fill_hover="#115ea3",
    button_primary_background_fill_hover_dark="#4f52b2",
    button_primary_background_fill_dark="#5b5fc7",
    button_primary_text_color="#ffffff",
    button_secondary_background_fill="#e0e0e0",
    button_secondary_background_fill_hover="#c0c0c0",
    button_secondary_background_fill_hover_dark="#a0a0a0",
    button_secondary_text_color="#000000",
    body_background_fill="#f5f5f5",
    block_background_fill="#ffffff",
    body_text_color="#242424",
    body_text_color_subdued="#616161",
    block_border_color="#d1d1d1",
    block_border_color_dark="#333333",
    input_background_fill="#ffffff",
    input_border_color="#d1d1d1",
    input_border_color_focus="#0f6cbd",
)

with gr.Blocks(theme=brand_theme, css="footer {visibility: hidden;}", fill_height=True) as demo:

    def clear_thread():
        global thread
        #thread = project_client.agents.create_thread() do later
        return []

    def on_example_clicked(evt: gr.SelectData):
        return evt.value["text"]  # Fill the textbox with that example text

    gr.HTML("<h1 style=\"text-align: center;\">Azure AI Agent Service</h1><h2 style=\"text-align: center;\">With Bing tool</h2>")

    chatbot = gr.Chatbot(
        type="messages",
        examples=[
            {"text": "What's my company's remote work policy?"},
            {"text": "Check if it will rain tomorrow in rome?"},
            {"text": "get the formula 1 championship standing and search all the information about the pilot at first place"},
            {"text": "Send my direct report a summary of the HR policy."},
        ],
        show_label=False,
        scale=1,
    )

    textbox = gr.Textbox(
        show_label=False,
        lines=1,
        submit_btn=True,
    )

    # Populate textbox when an example is clicked
    chatbot.example_select(fn=on_example_clicked, inputs=None, outputs=textbox)

    # On submit: call azure_enterprise_chat, then clear the textbox
    (textbox
     .submit(
         fn=azure_enterprise_chat,
         inputs=[textbox, chatbot],
         outputs=[chatbot, textbox],
     )
     .then(
         fn=lambda: "",
         outputs=textbox,
     )
    )

    # A "Clear" button that resets the thread and the Chatbot
    chatbot.clear(fn=clear_thread, outputs=chatbot)

# Launch your Gradio app
if __name__ == "__main__":
    demo.launch()