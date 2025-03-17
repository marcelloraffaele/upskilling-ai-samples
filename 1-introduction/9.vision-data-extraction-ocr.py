import base64
from mimetypes import guess_type
import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json

# Load the environment variables from the .env file
load_dotenv()

# Function to encode a local image into data URL 
def local_image_to_data_url(image_path):
    # Guess the MIME type of the image based on the file extension
    mime_type, _ = guess_type(image_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the image file
    with open(image_path, "rb") as image_file:
        base64_encoded_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
api_key = os.getenv("AZURE_OPENAI_API_KEY")  
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize Azure OpenAI Service client with key-based authentication    
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version= api_version)

# Example usage
image_path = '../data/images/receipt1.jpg'
data_url = local_image_to_data_url(image_path)
    
#Prepare the chat prompt 
chat_prompt = [
        { "role": "system", "content": "You are a helpful assistant." },
        { "role": "user", "content": [  
            { 
                "type": "text", 
                "text": "Please extract the text from this receipt, create a md file with data detail and a summary of all the relevant informations." 
            },
            { 
                "type": "image_url",
                "image_url": {
                    "url": data_url
                }
            }
        ] } 
    ] 
    
# Include speech result if speech is enabled  
messages = chat_prompt  


while True:
    
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=2000,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    
    #print(completion)
    #print()

    response = completion.choices[0].message.content
    #print(f"message: {completion.choices[0].message}")
    print(f"AI: {response}")

    messages.append({
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": response
            }
        ]
    })

    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_input
            }
        ]
    })