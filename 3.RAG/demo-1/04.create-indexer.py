from azure.search.documents.indexes.models import (
    SearchIndexer
)
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
data_source_name = "nasa-py-rag-tutorial-ds"
skillset_name = "nasa-py-rag-tutorial-ss"

# Create an indexer  
indexer_name = "nasa-py-rag-tutorial-idxr" 

indexer_parameters = None

indexer = SearchIndexer(  
    name=indexer_name,  
    description="Indexer to index documents and generate embeddings",  
    skillset_name=skillset_name,  
    target_index_name=index_name,  
    data_source_name=data_source_name,
    parameters=indexer_parameters
)  

# Create and run the indexer  
indexer_client = SearchIndexerClient(endpoint=search_endpoint, credential=AzureKeyCredential(search_key)    )  
indexer_result = indexer_client.create_or_update_indexer(indexer)  

print(f' {indexer_name} is created and running. Give the indexer a few minutes before running a query.') 