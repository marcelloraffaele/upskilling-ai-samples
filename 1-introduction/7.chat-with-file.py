import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from markitdown import MarkItDown

def extract_text_from_file(file):
    """
    Extracts text content from a given file using the MarkItDown library.
    Args:
        file (str): The path to the file from which text needs to be extracted.
    Returns:
        str: The extracted text content from the file.
    """
    md = MarkItDown()
    result = md.convert(file)
    return result.text_content

load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
api_key = os.getenv("AZURE_OPENAI_API_KEY")  
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version= api_version)

f1 = '../data/Modern hospitality resume.pdf'    #if you want to use your own file, change the path here

mdF1 = extract_text_from_file(file=f1)

#print(mdF1)

messages = [

    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an agent that given a file in markdown format will answer questions only about it. If you don't know the answer, you must say so. File: ---" + mdF1 + "---"
            }
        ]
    }
]


print("Welcome to chat with your file. Type 'exit' to end the conversation.")

while True:
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
    
    completion = client.chat.completions.create(
        model=deployment,
        messages=messages,
        max_tokens=800,
        temperature=0.7,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None,
        stream=False
    )
    
    response = completion.choices[0].message.content
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