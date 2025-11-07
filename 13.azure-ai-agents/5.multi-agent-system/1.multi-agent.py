import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ConnectedAgentTool, MessageRole
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()  # Use Azure Default Credential for authentication
)

with project_client:
    
    stock_price_agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="stock_price_bot",
        instructions="Your job is to get the stock price of a company. If you don't know the realtime stock price, return the last known stock price.",
        #tools=... # tools to help the agent get stock prices
    )

    connected_agent = ConnectedAgentTool(
        id=stock_price_agent.id, name=stock_price_agent.name, description="Gets the stock price of a company"
    )
    
    # Create an agent with translation instructions
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
        name="stock-price-coordinator-agent",  # Name of the agent
        instructions="You are a helpful agent, and use the available tools to get stock prices.",
        tools=connected_agent.definitions,
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Create message to thread
    message = project_client.agents.messages.create(
        thread_id=thread.id,
        role=MessageRole.USER,
        content="What is the stock price of Microsoft?",
    )
    print(f"Created message, ID: {message.id}")

    # Create and process Agent run in thread with tools
    run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
    print(f"Run finished with status: {run.status}")

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")

    # Print the Agent's response message with optional citation
    response_message = project_client.agents.messages.get_last_message_by_role(
        thread_id=thread.id, role=MessageRole.AGENT
    )
    if response_message:
        for text_message in response_message.text_messages:
            print(f"Agent response: {text_message.text.value}")
        for annotation in response_message.url_citation_annotations:
            print(f"URL Citation: [{annotation.url_citation.title}]({annotation.url_citation.url})")
    
    
    # Delete the Agent when done
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")

    # Delete the connected Agent when done
    project_client.agents.delete_agent(stock_price_agent.id)
    print("Deleted connected agent")