from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.devui import serve
import os
import asyncio
from azure.identity import AzureCliCredential
from agent_framework.azure import AzureOpenAIResponsesClient
from agent_framework import tool
from pydantic import Field
from typing import Annotated
from random import randint

from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

@tool(approval_mode="never_require")
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."



credential = AzureCliCredential()

client = AzureOpenAIResponsesClient(
    project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    deployment_name=os.environ["MODEL_DEPLOYMENT_NAME"],
    credential=credential,
)

agent = client.as_agent(
    name="WeatherAgent",
    instructions="You are a friendly assistant. Keep your answers brief.",
    tools=[get_weather],
)

# Launch DevUI
serve(entities=[agent], auto_open=True)
# Opens browser to http://localhost:8080



