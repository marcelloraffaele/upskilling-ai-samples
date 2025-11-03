from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizableTextQuery
from azure.search.documents.indexes import SearchIndexerClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_AI_SEARCH_API_KEY")
index_name = "nasa-py-rag-tutorial-idx"

# Vector Search using text-to-vector conversion of the query string
query = "what's NASA's website?"  

search_client = SearchClient(endpoint=search_endpoint, credential=AzureKeyCredential(search_key), index_name=index_name)
vector_query = VectorizableTextQuery(text=query, k_nearest_neighbors=50, fields="text_vector")
  
results = search_client.search(  
    search_text=query,  
    vector_queries= [vector_query],
    select=["chunk"],
    top=1
)  
  
for result in results:  
    print(f"Score: {result['@search.score']}")
    print(f"Chunk: {result['chunk']}")