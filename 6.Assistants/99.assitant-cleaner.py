import os
from openai import AzureOpenAI
from dotenv import load_dotenv

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

# Delete all assistants and files
file_list = client.files.list(purpose=['assistants', 'assistant_outputs'])
file_count = len(file_list.data)
print(f"There are {file_count} files present.")

if file_count > 0:
    confirm = input("Do you want to delete all files and assistants? (y/n): ").strip().lower()
    if confirm in ['y', 'yes']:
        print("Proceeding with files deletion...")
        #print(file_list)
        for file in file_list:  
            deleted = client.files.delete(file.id)
            print("file deleted: " + file.id + " " + str(deleted))

# Print the number of assistants found
assistant_list = client.beta.assistants.list()
#print(assistant_list)
assistant_count = len(assistant_list.data)
print(f"There are {assistant_count} assistants present.")

if assistant_count > 0:
    confirm_assistants = input("Do you want to delete all assistants? (y/n): ").strip().lower()
    if confirm_assistants in ['y', 'yes']:
        print("Proceeding with assistants deletion...")
        
        for assistant in assistant_list:  
            deleted = client.beta.assistants.delete(assistant.id)
            print("assistant deleted: " + assistant.id + " " + str(deleted))