import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
api_key = os.getenv("AZURE_OPENAI_API_KEY")  
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")  
search_key = os.getenv("AZURE_AI_SEARCH_API_KEY")
search_index = "aifoundry-cv-index"

# Initialize Azure OpenAI Service client with key-based authentication    
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version= api_version)
    
completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "system",
            "content": "You are an AI assistant that helps people find information. The user is interested only in indexed data source. if no answer is found, please provide a message to the user.",
        },
        {
            "role": "user",
            "content": "Find a UI/UX designer in New York. answer in only 100 words",
        },
    ],
    extra_body={
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_endpoint,
                    "index_name": search_index,
                    "authentication": {
                        "type": "api_key",
                        "key": search_key
                    }
                }
            }
        ]
    }
)

#print(completion.model_dump_json(indent=2))

content = completion.choices[0].message.content
print("AI: " + content)

print("Citations:")
context = completion.choices[0].message.context
for citation_index, citation in enumerate(context["citations"]):
    citation_reference = f"[doc{citation_index + 1}]"
    filepath = citation["filepath"]
    title = citation["title"]
    chunk_id = citation["chunk_id"]
    citationTxt = f"ref='{citation_reference}' title='{title} (See from file {filepath}, Part {chunk_id})"
    print(citationTxt)