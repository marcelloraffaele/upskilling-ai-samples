import os
import asyncio
from azure.identity import AzureCliCredential
from agent_framework.azure import AzureOpenAIResponsesClient

from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

async def main():
    credential = AzureCliCredential()
    
    client = AzureOpenAIResponsesClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        deployment_name=os.environ["MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    )

    agent = client.as_agent(
        name="HelloAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
    )

    # Non-streaming: get the complete response at once
    result = await agent.run("What is the largest city in Italy?")
    print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main())