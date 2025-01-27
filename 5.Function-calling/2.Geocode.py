import os
import json
from openai import AzureOpenAI
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
import requests
import sys

# Load the environment variables from the .env file
load_dotenv()

openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
deployment_name = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
api_key = os.getenv("AZURE_OPENAI_API_KEY")  
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize Azure OpenAI Service client with key-based authentication    
client = AzureOpenAI(
    azure_endpoint=openai_endpoint,
    api_key=api_key,
    api_version= api_version)


def get_geocode(location):
    """Get the coordinates (latitude, longitude, elevation, timezone, population, country) of a location using a geocoding API."""
    
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get("results"):
            ret = json.dumps(data.get("results")[0])
            print(f"DEBUG: get_geocode({location})= {ret}")
            return ret
    return json.dumps({"location": location, "error": "Unable to fetch geocode"})

def run_conversation(question):
    # Initial user message
    messages = [{"role": "user", "content": question}] # Parallel function call with a single tool/function defined

    # Define the function for the model
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_geocode",
                "description": "Get the coordinates (latitude, longitude, elevation, timezone, population, country) of a location using a geocoding API.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city name, e.g. San Francisco",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the function
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message)

    #print("Model's response:")  
    #print(response_message)  

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.function.name == "get_geocode":
                function_args = json.loads(tool_call.function.arguments)
                print(f"Function arguments: {function_args}")  
                time_response = get_geocode(
                    location=function_args.get("location")
                )
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": "get_geocode",
                    "content": time_response,
                })
    else:
        print("No tool calls were made by the model.")  

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
    )

    return final_response.choices[0].message.content


while True:
    user_input = input("Enter a location (or 'q' to quit): ")
    if user_input.lower() in ['q', 'quit']:
        break
    print(run_conversation(user_input))

