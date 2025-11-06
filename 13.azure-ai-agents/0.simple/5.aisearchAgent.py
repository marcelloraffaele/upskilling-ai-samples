#https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/azure-ai-search?tabs=keys%2Cazurecli
import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
# import the folloing 
from azure.ai.agents.models import AzureAISearchTool, AzureAISearchQueryType
from azure.ai.projects.models import ConnectionType

from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()


# Retrieve the project endpoint from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]
model_name = os.environ["MODEL_DEPLOYMENT_NAME"]


with AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(exclude_interactive_browser_credential=False)
) as project_client:
    agents_client = project_client.agents

    # Define the Azure AI Search connection ID and index name
    azure_ai_conn_id = project_client.connections.get(name=os.environ["AZURE_AI_SEARCH_CONNECTION_NAME"]).id

    # Find the index name on the Search Management > Indexes page of your Azure AI Search service
    index_name = "hr-demo-index"

    # Initialize the Azure AI Search tool
    ai_search = AzureAISearchTool(
        index_connection_id=azure_ai_conn_id,
        index_name=index_name,
        query_type=AzureAISearchQueryType.SIMPLE,  # Use SIMPLE query type
        top_k=3,  # Retrieve the top 3 results
        filter="",  # Optional filter for search results
    )

    # Create an agent and run user's request with function calls
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="aisearch-agent",
        instructions="You are a helpful agent that uses Azure AI Search to answer user queries based on the provided index data.",
        tools=ai_search.definitions,
        tool_resources=ai_search.resources
    )
    print(f"Created agent, ID: {agent.id}")

    thread = agents_client.threads.create()
    print(f"Created thread, ID: {thread.id}")

    while True:
        user_input = input("Enter a command for your api (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        message = agents_client.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        print(f"Created message, ID: {message.id}")

        # Create and automatically process the run, handling tool calls internally
        run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
        print(f"Run finished with status: {run.status}")

        if run.status == "failed":
            print(f"Run failed: {run.last_error}")
            break

        # Retrieve the steps taken during the run for analysis
        run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)

        
        # Fetch and log all messages
        #messages = project_client.agents.messages.list(thread_id=thread.id)
        #for message in messages:
        #    print(f"Role: {message.role}, Content: {message.content}")
        answer = project_client.agents.messages.get_last_message_by_role(thread_id=thread.id, role="assistant")
        print(f"answer from assistant: {answer.content[0].text.value}")


    # Delete the agent after use
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")