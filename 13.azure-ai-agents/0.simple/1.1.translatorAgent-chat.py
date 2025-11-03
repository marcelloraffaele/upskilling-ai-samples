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
    agent = project_client.agents.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],  # Model deployment name
        name="english-translator-agent",  # Name of the agent
        instructions="You are a helpful agent that translates text to English. Translate all the message that the user will write.",  # Instructions for the agent
    )
    print(f"Created agent, ID: {agent.id}")

    # Create a thread for communication
    thread = project_client.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    while True:
        user_input = input("Enter text to translate (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        # Add a message to the thread
        message = project_client.agents.messages.create(
            thread_id=thread.id,
            role="user",  # Role of the message sender
            content=user_input,  # Message content
        )
        print(f"Created message, ID: {message['id']}")

        # Create and process an agent run
        run = project_client.agents.runs.create_and_process(
            thread_id=thread.id,
            agent_id=agent.id
        )
        print(f"Run finished with status: {run.status}")

        # Check if the run failed
        if run.status == "failed":
            print(f"Run failed: {run.last_error}")
            break

        # Fetch and log all messages
        message = project_client.agents.messages.get_last_message_by_role(thread_id=thread.id, role="assistant")
        print(f"Translated text: {message.content[0].text}")
    
    
#    project_client.agents.delete_agent(agent.id)
#    print("Deleted agent")