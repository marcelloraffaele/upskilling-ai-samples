import os, time, json, logging
from typing import Optional,Any, List, Dict
from azure.ai.projects import AIProjectClient
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import BingGroundingTool, MessageRole, ThreadMessage, ToolSet, ThreadRun, RunStep, RunStepDeltaChunk, MessageDeltaChunk, AgentStreamEvent, AgentEventHandler

def get_logger(name: str = "my_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

from dotenv import load_dotenv
load_dotenv()

logger = get_logger()



class LoggingToolSet(ToolSet):

    def execute_tool_calls(self, tool_calls: List[Any]) -> Any:
        result = super().execute_tool_calls(tool_calls)
        # Custom logic: log or store the result
        logger.info(f"-------------->Tool calls: {tool_calls}, Output: {result}")
        return result

class RichToolSet(ToolSet):
    def execute_tool_calls(self, tool_calls: list) -> list:
        """
        Returns a list of dicts, each containing:
         - tool_call input
         - raw tool output
         - metadata like execution time
        """
        from time import perf_counter

        enriched_outputs = []
        for tc in tool_calls:
            start = perf_counter()
            # Here, you might want to call some single-tool execution
            output = super().execute_tool_calls([tc])
            end = perf_counter()
            enriched_outputs.append({
                "tool_call": tc,
                "output": output,
                "elapsed_seconds": end - start
            })
        return enriched_outputs


def fetch_and_print_new_agent_response(
    thread_id: str,
    agents_client: AgentsClient,
    last_message_id: Optional[str] = None,
) -> Optional[str]:
    response = agents_client.messages.get_last_message_by_role(
        thread_id=thread_id,
        role=MessageRole.AGENT,
    )

    #if response:
    #    print(f"response dump={json.dumps(response.as_dict(), indent=2)}")

    if not response or response.id == last_message_id:
        return last_message_id  # No new content

    print("\nAgent response:")
    print("\n".join(t.text.value for t in response.text_messages))

    for ann in response.url_citation_annotations:
        print(f"URL Citation: [{ann.url_citation.title}]({ann.url_citation.url})")

    return response.id

def create_research_summary(
        message : ThreadMessage,
        filepath: str = "research_summary.md"
) -> None:
    if not message:
        print("No message content provided, cannot create research summary.")
        return

    with open(filepath, "w", encoding="utf-8") as fp:
        # Write text summary
        text_summary = "\n\n".join([t.text.value.strip() for t in message.text_messages])
        fp.write(text_summary)

        # Write unique URL citations, if present
        if message.url_citation_annotations:
            fp.write("\n\n## References\n")
            seen_urls = set()
            for ann in message.url_citation_annotations:
                url = ann.url_citation.url
                title = ann.url_citation.title or url
                if url not in seen_urls:
                    fp.write(f"- [{title}]({url})\n")
                    seen_urls.add(url)

    print(f"Research summary written to '{filepath}'.")


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

toolset = RichToolSet()
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

        # Create message to thread
        message = agents_client.messages.create(
            thread_id=thread.id,
            role="user",  # Role of the message sender
            content="get the latest weather forecast in rome",  # Message content
        )
        print(f"Created message, ID: {message['id']}")

        
        
#        run = agents_client.runs.create(thread_id=thread.id, agent_id=agent.id)
#
#        last_message_id = None
#        while run.status in ("queued", "in_progress"):
#            time.sleep(1)
#            run = agents_client.runs.get(thread_id=thread.id, run_id=run.id)
#
#            #print(f"run dump={json.dumps(run.as_dict(), indent=2)}")
#
#            last_message_id = fetch_and_print_new_agent_response(
#                thread_id=thread.id,
#                agents_client=agents_client,
#                last_message_id=last_message_id,
#            )
#            print(f"Run status: {run.status}")
#
#        print(f"Run finished with status: {run.status}, ID: {run.id}")
#
#        if run.status == "failed":
#            print(f"Run failed: {run.last_error}")
#
#        # Fetch the final message from the agent in the thread and create a research summary
#        final_message = agents_client.messages.get_last_message_by_role(
#            thread_id=thread.id, 
#            role=MessageRole.AGENT
#        )
#        if final_message:
#            create_research_summary(final_message)

        # Create and process an agent run
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id,
            toolset=toolset,
            #tool_choice={"type": "bing_grounding"}  # optional, you can force the model to use Grounding with Bing Search tool
        )
        print(f"Run finished with status: {run.status}")

        # Check if the run failed
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")

        # Fetch and log all messages
        messages = project_client.agents.messages.list(thread_id=thread.id)
        for message in messages:
            print(f"Role: {message.role}, Content: {message.content}")

        run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)
        for step in run_steps:
            print(f"Step {step['id']} status: {step['status']}")

            # Check if there are tool calls in the step details
            step_details = step.get("step_details", {})
            
            tool_calls = step_details.get("tool_calls", [])

            if tool_calls:
                print("  Tool calls:")
                for call in tool_calls:
                    print(f"    Tool Call ID: {call.get('id')}")
                    print(f"    Type: {call.get('type')}")

                    function_details = call.get("function", {})
                    if function_details:
                        print(f"    Function name: {function_details.get('name')}")
            print()  # add an extra newline between steps

        # Clean-up and delete the agent once the run is finished.
        # NOTE: Comment out this line if you plan to reuse the agent later.
        agents_client.delete_agent(agent.id)
        print("Deleted agent")