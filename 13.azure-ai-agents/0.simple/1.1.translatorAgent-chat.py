import os
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import PromptAgentDefinition

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

    agentName = "english-translator-agent"

    agent = None
    try:
        # Check if the agent already exists
        agentDetails = project_client.agents.get(agentName)
        if agentDetails is not None and agentDetails.versions is not None:
            version = agentDetails.versions.latest.version
            agent = project_client.agents.get_version(agentName, version)
    except Exception as e:
        agent = None

    if agent is None:
        agent = project_client.agents.create_version(
            agent_name=agentName,
            definition=PromptAgentDefinition(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                instructions="You are a helpful agent that translates text to English. Translate all the message that the user will write.",  # Instructions for the agent
            ),
        )

    print(f"Agent {agentName} already exists, ID: {agent.id}, version: {agent.version}")

    openai_client = project_client.get_openai_client()

    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    while True:
        user_input = input("Enter text to translate (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        
        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{"type": "message", "role": "user", "content": user_input}],
        )

        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "version": agent.version, "type": "agent_reference"}},
        )

        print(f"Translated text: {response.output_text}")


    
    
#    project_client.agents.delete_agent(agent.id)
#    print("Deleted agent")