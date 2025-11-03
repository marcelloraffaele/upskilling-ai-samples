import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import FunctionTool, ToolSet, ListSortOrder

from azure.search.documents.agent import KnowledgeAgentRetrievalClient
from azure.search.documents.agent.models import KnowledgeAgentRetrievalRequest, KnowledgeAgentMessage, KnowledgeAgentMessageTextContent
from azure.ai.agents.models import AgentsNamedToolChoice, AgentsNamedToolChoiceType, FunctionName
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

def agentic_retrieval() -> str:
    """
        Searches a NASA e-book about images of Earth at night and other science related facts.
        The returned string is in a JSON format that contains the reference id.
        Be sure to use the same format in your agent's response
        You must refer to references by id number
    """
    # Take the last 5 messages in the conversation
    messages = project_client.agents.messages.list(thread.id, limit=5, order=ListSortOrder.DESCENDING)
    # Reverse the order so the most recent message is last
    messages = list(messages)
    messages.reverse()
    retrieval_result = agent_client.retrieve(
        retrieval_request=KnowledgeAgentRetrievalRequest(
            messages=[
                    KnowledgeAgentMessage(
                        role=m["role"],
                        content=[KnowledgeAgentMessageTextContent(text=m["content"])]
                    ) for m in messages if m["role"] != "system"
            ]
        )
    )

    # Associate the retrieval results with the last message in the conversation
    last_message = messages[-1]
    retrieval_results[last_message.id] = retrieval_result

    # Return the grounding response to the agent
    return retrieval_result.response[0].content[0].text


agent_name = "rag-agent"
instructions = """
A Q&A agent that can answer questions about the Earth at night.
Sources have a JSON format with a ref_id that must be cited in the answer using the format [ref_id].
If you do not have the answer, respond with "I don't know".
"""

search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_AI_SEARCH_API_KEY")

# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()  # Use Azure Default Credential for authentication
)

with project_client:
    # Create an agent with translation instructions
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
        name=agent_name,  # Name of the agent
        instructions=instructions,  # Instructions for the agent
    )
    print(f"Created agent, ID: {agent.id}")

    agent_client = KnowledgeAgentRetrievalClient(endpoint=search_endpoint, agent_name=agent_name, credential=AzureKeyCredential(search_key))

    thread = project_client.agents.threads.create()
    retrieval_results = {}

    # AGENTIC RETRIEVAL DEFINITION "LIFTED AND SHIFTED" TO NEXT SECTION

    functions = FunctionTool({ agentic_retrieval })
    toolset = ToolSet()
    toolset.add(functions)
    project_client.agents.enable_auto_function_calls(toolset)



    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="""
            Why do suburban belts display larger December brightening than urban cores even though absolute light levels are higher downtown?
            Why is the Phoenix nighttime street grid is so sharply visible from space, whereas large stretches of the interstate between midwestern cities remain comparatively dim?
        """
    )

    run = project_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
        tool_choice=AgentsNamedToolChoice(type=AgentsNamedToolChoiceType.FUNCTION, function=FunctionName(name="agentic_retrieval")),
        toolset=toolset)
    if run.status == "failed":
        raise RuntimeError(f"Run failed: {run.last_error}")
    output = project_client.agents.messages.get_last_message_text_by_role(thread_id=thread.id, role="assistant").text.value

    print("Agent response:", output.replace(".", "\n"))
    
#    project_client.agents.delete_agent(agent.id)
#    print("Deleted agent")