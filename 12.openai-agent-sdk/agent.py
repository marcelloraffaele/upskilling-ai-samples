import asyncio
import random
from agents import Agent, Runner, function_tool, set_default_openai_client, set_default_openai_api, set_tracing_disabled
from dotenv import load_dotenv
import os
from openai import AsyncAzureOpenAI
import json


@function_tool
def get_random_numbers() -> list[int]:
    """Generate a random array of 10 numbers."""
    print("Generating random numbers...")
    return [random.randint(0, 100) for _ in range(10)]



async def main():

    load_dotenv()

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
    api_key = os.getenv("AZURE_OPENAI_API_KEY")  
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    # Initialize Azure OpenAI client
    openai_client = AsyncAzureOpenAI(
        api_key= api_key,
        api_version=api_version,
        azure_endpoint=endpoint,
        azure_deployment=deployment
    )

    # Set the default OpenAI client for the Agents SDK
    set_default_openai_client(client=openai_client, use_for_tracing=False)
    set_default_openai_api("chat_completions")
    set_tracing_disabled(disabled=True)

    agent = Agent(
        name="RandomNumberAgent",
        instructions="You are an agent that provides random numbers.",
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"),
        tools=[get_random_numbers]
    )

    result = await Runner.run(agent, input="Generate 10 random numbers.")
    print(result.final_output)

#    prompt = "Generate a list of 10 random numbers between 0 and 100."
#    response = await openai_client.chat.completions.create(
#        model=deployment,
#        messages=[
#            {"role": "system", "content": "You are a helpful assistant."},
#            {"role": "user", "content": prompt}
#        ]
#    )
#
#    # Extract and print the response
#    random_numbers = response
#    print("Generated Random Numbers:", json.dumps(random_numbers, indent=2))

    
if __name__ == "__main__":
    asyncio.run(main())