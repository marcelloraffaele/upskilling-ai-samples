from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import ListSortOrder
import os
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

# Create an Azure AI Client from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

project = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=project_endpoint
)

agent = project.agents.get_agent("asst_UlLVhH8j8Ut0Ln5sKRVfvpYv")

thread = project.agents.threads.create()
print(f"Created thread, ID: {thread.id}")

while True:
     user_input = input("You: ")
     if user_input.lower() in ["exit", "quit"]:
         break

     message = project.agents.messages.create(
         thread_id=thread.id,
         role="user",
         content=user_input
     )

     run = project.agents.runs.create_and_process(
         thread_id=thread.id,
         agent_id=agent.id)

     if run.status == "failed":
         print(f"Run failed: {run.last_error}")
     else:
         messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

         for message in messages:
             if message.text_messages:
                 print(f"{message.role}: {message.text_messages[-1].text.value}")
