from azure.search.documents.indexes import SearchIndexerClient
from azure.search.documents.indexes.models import (
    SearchIndexerDataContainer,
    SearchIndexerDataSourceConnection
)
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
search_key = os.getenv("AZURE_AI_SEARCH_API_KEY")
AZURE_STORAGE_CONNECTION = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

# Create a data source 
indexer_client = SearchIndexerClient(endpoint=search_endpoint, credential=AzureKeyCredential(search_key))
container = SearchIndexerDataContainer(name="nasa-ebooks-pdfs-all")
data_source_connection = SearchIndexerDataSourceConnection(
    name="nasa-py-rag-tutorial-ds",
    type="azureblob",
    connection_string=AZURE_STORAGE_CONNECTION,
    container=container
)
data_source = indexer_client.create_or_update_data_source_connection(data_source_connection)

print(f"Data source '{data_source.name}' created or updated")