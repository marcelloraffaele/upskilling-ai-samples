import os
import json
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam, ChatCompletionToolParam
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

endpoint = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
model = os.getenv("OLLAMA_MODEL", "llama3.2")

print(f"Using Ollama endpoint: {endpoint}, model: {model}")

client = OpenAI(
    base_url=endpoint,
    api_key="ollama")  # Required by the SDK, ignored by local Ollama.

# Simplified timezone data
TIMEZONE_DATA = {
    "tokyo": "Asia/Tokyo",
    "san francisco": "America/Los_Angeles",
    "paris": "Europe/Paris",
    "rome": "Europe/Rome",
}

def get_current_time(location):
    """Get the current time for a given location"""

    print(f"START: get_current_time called with location: {location}")  
    location_lower = location.lower()
    
    for key, timezone in TIMEZONE_DATA.items():
        if key in location_lower:
            
            current_time = datetime.now(ZoneInfo(timezone)).strftime("%I:%M %p")
            print(f"STOP: Timezone found for {key} with timezone {current_time}")  
            return json.dumps({
                "location": location,
                "current_time": current_time
            })
    
    print(f"STOP: No timezone data found for {location_lower}")  
    return json.dumps({"location": location, "current_time": "unknown"})

def run_conversation():
    # Initial user message
    #messages = [{"role": "user", "content": "What's the current time in San Francisco"}] # Single function call
    messages: list[ChatCompletionMessageParam] = [
        {
            "role": "system",
            "content": (
                "Use get_current_time separately for each requested city. "
                "Each tool call must contain exactly one city in location. "
                "Only report times returned by the tool; do not calculate or guess times."
            ),
        },
        {"role": "user", "content": "What's the current time in San Francisco, Tokyo, and Rome?"}
    ]

    # Define the function for the model
    tools: list[ChatCompletionToolParam] = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current time in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Exactly one city name, e.g. San Francisco. Never combine cities.",
                        },
                    },
                    "required": ["location"],
                },
            }
        }
    ]

    # First API call: Ask the model to use the function
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        stream=False,
    )

    # Process the model's response
    response_message = response.choices[0].message
    messages.append(response_message.model_dump(exclude_unset=True))

    print("Model's response:")  
    print(response_message)  

    # Handle function calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.type != "function" or tool_call.function.name != "get_current_time":
                raise ValueError(f"Ollama returned an unsupported tool call: {tool_call}")
            function_args = json.loads(tool_call.function.arguments)
            if not isinstance(function_args, dict):
                raise ValueError("get_current_time arguments must be a JSON object.")
            location = function_args.get("location")
            if not isinstance(location, str) or not location.strip():
                raise ValueError("get_current_time requires a non-empty location string.")
            time_response = get_current_time(location=location)
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "content": time_response,
            })
    else:
        print("No tool calls were made by the model.")
        if response_message.content is None:
            raise RuntimeError("Ollama returned a response without text or tool calls.")
        return response_message.content

    # Second API call: Get the final response from the model
    final_response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=False,
    )

    content = final_response.choices[0].message.content
    if content is None:
        raise RuntimeError("Ollama returned a final response without text.")
    return content

# Run the conversation and print the result
if __name__ == "__main__":
    print(run_conversation())