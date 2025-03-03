import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from enum import Enum

class ModelType(Enum):
    OPENAI = "openai"
    DEEPSEEK = "deepseek"
    PHI = "phi"

load_dotenv()

def completion(messageList, modelType):
    if modelType == ModelType.OPENAI:
        client = openaiClient(messageList)
    
    elif modelType == ModelType.DEEPSEEK:
        client = deepseekclient(messageList)
    
    #elif modelType == ModelType.PHI:
    else:
        client = phiClient(messageList)
    
    payload = {
        "messages": messageList,
        "max_tokens": 2048
    }
    response = client.complete(payload)
    return response.choices[0].message.content

def deepseekclient(messageList):
    print("In completion: " + str(messageList))

    endpoint = os.getenv("DEEPSEEK_ENDPOINT") 
    api_key = os.getenv("DEEPSEEK_API_KEY", '')
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )
    return client
    

def openaiClient(messageList):
    print("In completion: " + str(messageList))

    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
    deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
    api_key = os.getenv("AZURE_OPENAI_API_KEY")  
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")

    client = ChatCompletionsClient(
        endpoint=endpoint + "/openai/deployments/" + deployment,
        credential=AzureKeyCredential(api_key)
    )

    return client

def phiClient(messageList):
    print("In completion: " + str(messageList))

    endpoint = os.getenv("PHI_ENDPOINT") 
    api_key = os.getenv("PHI_API_KEY", '')
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(api_key)
    )
    return client