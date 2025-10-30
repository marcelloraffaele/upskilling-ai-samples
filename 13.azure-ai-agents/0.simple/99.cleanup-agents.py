import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
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
    # Create an agent with translation instructions
    agents = project_client.agents.list_agents()
    for agent in agents:
        if agent.name in ["my-agent"]:
            print(f"Deleting agent ID: {agent.id}, Name: {agent.name}")
            project_client.agents.delete_agent(agent.id)