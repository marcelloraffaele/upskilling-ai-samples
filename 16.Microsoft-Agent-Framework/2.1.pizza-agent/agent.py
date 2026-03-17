import os
import asyncio
from azure.identity import AzureCliCredential
from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework import tool
from pydantic import Field
from typing import Annotated
from random import randint
from PizzaTools import PizzaTools

from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()


async def main():

    tools = PizzaTools(safe=True)

    credential = AzureCliCredential()
    
    client = AzureOpenAIResponsesClient(
        project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        deployment_name=os.environ["MODEL_DEPLOYMENT_NAME"],
        credential=credential,
    )

    agent = client.as_agent(
        name="PizzaAgent",
        instructions="You are a friendly assistant. Keep your answers brief.",
        tools=[tools.get_pizza_menu, tools.add_pizza_to_cart, tools.remove_pizza_from_cart, tools.get_pizza_from_cart, tools.get_cart, tools.checkout],
    )

    # Non-streaming: get the complete response at once
    result = await agent.run("What is the pizza menu?")
    print(f"Agent: {result}")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the chat.")
            break

        result = await agent.run(user_input)
        print(f"Agent: {result}")

if __name__ == "__main__":
    asyncio.run(main())