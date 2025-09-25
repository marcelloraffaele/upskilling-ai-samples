import os, sys,json
from typing import Optional,Any, List, Dict
from azure.ai.projects import AIProjectClient
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import BingGroundingTool, MessageRole, ThreadMessage, ToolSet, ThreadRun, RunStep, RunStepDeltaChunk, MessageDeltaChunk, AgentStreamEvent, AgentEventHandler,MessageTextContent

from dotenv import load_dotenv
load_dotenv()

class MyEventHandler(AgentEventHandler):
    def __init__(self):
        super().__init__()
        self._current_message_id = None
        self._accumulated_text = ""

    def on_message_delta(self, delta: MessageDeltaChunk) -> None:
        # If a new message id, start fresh
        if delta.id != self._current_message_id:
            # First, if we had an old message that wasn't completed, finish that line
            if self._current_message_id is not None:
                print()  # move to a new line
            
            self._current_message_id = delta.id
            self._accumulated_text = ""
            print("\nassistant > ", end="")  # prefix for new message

        # Accumulate partial text
        partial_text = ""
        if delta.delta.content:
            for chunk in delta.delta.content:
                partial_text += chunk.text.get("value", "")
        self._accumulated_text += partial_text

        # Print partial text with no newline
        print(partial_text, end="", flush=True)

    def on_thread_message(self, message: ThreadMessage) -> None:
        # When the assistant's entire message is "completed", print a final newline
        if message.status == "completed" and message.role == "assistant":
            print()  # done with this line
            self._current_message_id = None
            self._accumulated_text = ""
        else:
            # For other roles or statuses, you can log if you like:
            print(f"{message.status.name.lower()} (id: {message.id})")

    def on_thread_run(self, run: ThreadRun) -> None:
        print(f"status > {run.status.name.lower()}")
        if run.status == "failed":
            print(f"error > {run.last_error}")

    def on_run_step(self, step: RunStep) -> None:
        print(f"{step.type.name.lower()} > {step.status.name.lower()}")

    def on_run_step_delta(self, delta: RunStepDeltaChunk) -> None:
        # If partial tool calls come in, we log them
        if delta.delta.step_details and delta.delta.step_details.tool_calls:
            for tcall in delta.delta.step_details.tool_calls:
                if getattr(tcall, "function", None):
                    if tcall.function.name is not None:
                        print(f"tool call > {tcall.function.name}")

    def on_unhandled_event(self, event_type: str, event_data):
        print(f"unhandled > {event_type} > {event_data}")

    def on_error(self, data: str) -> None:
        print(f"error > {data}")

    def on_done(self) -> None:
        print("done")

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
bing = BingGroundingTool(connection_id=conn_id)


with project_client:

    with project_client.agents as agents_client:

        # Create an agent with the Bing Grounding tool
        agent = agents_client.create_agent(
            model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
            name="my-agent",  # Name of the agent
            instructions="You are a helpful agent.",  # Instructions for the agent
            tools=bing.definitions,
        )
        # [END create_agent_with_deep_research_tool]
        print(f"Created agent, ID: {agent.id}")

        # Create thread for communication
        thread = agents_client.threads.create()
        print(f"Created thread, ID: {thread.id}")

        # Create message to thread
        message = agents_client.messages.create(
            thread_id=thread.id,
            role="user",  # Role of the message sender
            content="get the formula 1 championship standing and search all the information about the pilot at first place",  # Message content
        )
        print(f"Created message, ID: {message['id']}")

        
        with agents_client.runs.stream(
            thread_id=thread.id,
            agent_id=agent.id,
            event_handler=MyEventHandler()
            ) as stream:
            for event_type, event_data, func_return in stream:

                # Debug print of all events
                #if not isinstance(event_data, MessageDeltaChunk):
                #    #print(f"\n[Generic] event_type={event_type} dump={json.dumps(event_data.as_dict(), indent=2)}") 
                #    print(f">> {json.dumps(event_data.as_dict())}")

                # text deltas (incremental content)
                if isinstance(event_data, MessageDeltaChunk):
                    # smaller text chunks while agent generates content
                    sys.stdout.write(event_data.text or "")
                    sys.stdout.flush()

                # A fully created message object
                elif isinstance(event_data, ThreadMessage):
                    print(f"\n[Message created] id={event_data.id} status={event_data.status} role={event_data.role} messssage={event_data.content[-1].text.value if event_data.content and isinstance(event_data.content[-1], MessageTextContent) else '<non-text>'}")

                # Run-level changes: status, required_action, id, etc.
                elif isinstance(event_data, ThreadRun):
                    print(f"\n[Run] id={event_data.id}, status={event_data.status}")
                    #print(f"\n[Runx] rundump={json.dumps(event_data.as_dict())}")
                    # If the run requests actions (e.g. function/tool outputs), handle them:
                    if getattr(event_data, "status", None) == "requires_action":
                        required = getattr(event_data, "required_action", None)
                        if required and getattr(required, "type", "") == "submit_tool_outputs":
                            # required.submit_tool_outputs.tool_calls contains tool-call descriptors
                            tool_calls = required.submit_tool_outputs.tool_calls
                            # Example: build tool_outputs by "executing" each requested tool locally
                            tool_outputs = []
                            for tc in tool_calls:
                                print(f"Agent requested tool call id={tc.id} name={getattr(tc, 'function', {}).get('name', '<unknown>')}")
                                # TODO: run the actual local function/tool using tc.function.parameters
                                # Here we send a placeholder; replace with real function execution
                                tool_outputs.append({"tool_call_id": tc.id, "output": "RESULT_FROM_LOCAL_TOOL"})

                            # Submit the tool outputs so the run can continue
                            print("Submitting tool outputs back to run...")
                            agents_client.runs.submit_tool_outputs(thread_id=thread.id, run_id=event_data.id, tool_outputs=tool_outputs)
                            print("Submitted tool outputs.")

                # Specific run step updates (e.g., a step that is calling tools)
                elif isinstance(event_data, RunStep):
                    print(f"[RunStep] type={event_data.type} status={event_data.status}")
                    #print(f" event_data= {json.dumps(event_data.as_dict())}")

                elif event_type == AgentStreamEvent.ERROR:
                    print("[STREAM ERROR]", event_data)

                elif event_type == AgentStreamEvent.DONE:
                    print("\n[STREAM DONE]")
                    break




        # Clean-up and delete the agent once the run is finished.
        # NOTE: Comment out this line if you plan to reuse the agent later.
        agents_client.delete_agent(agent.id)
        print("Deleted agent")