import os
import asyncio
from agent_framework import Agent
from agent_framework.ollama import OllamaChatClient
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
    
    agent = Agent(
        client=OllamaChatClient(
            model_id=os.environ["OLLAMA_MODEL"]
        ),        
        name="PizzaAgent",
        instructions="You are a pizza agent, you help user to take orders. Answer always with the language of the user's input.",
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