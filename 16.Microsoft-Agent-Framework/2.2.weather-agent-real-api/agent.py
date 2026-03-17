import os
import asyncio
from azure.identity import AzureCliCredential
from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework import tool
from pydantic import Field
from typing import Annotated
from random import randint
from WeatherTools import WeatherTools

from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()


async def main():

    tools = WeatherTools(enableDebug=True)

    credential = AzureCliCredential()
    
    client = AzureOpenAIResponsesClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        deployment_name=os.environ["MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    )

    agent = client.as_agent(
        name="WeatherAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
        tools=[tools.get_geocode, tools.get_forecast],
    )

    # Non-streaming: get the complete response at once
#    result = await agent.run("What is the weather forecast for Rome?")
#    print(f"Agent: {result}")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat.")
            break

        result = await agent.run(user_input)
        print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main())