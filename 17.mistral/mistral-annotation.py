import os, json
from mistralai.azure.client import MistralAzure

import base64
from mimetypes import guess_type

from mistralai.extra import response_format_from_pydantic_model

from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

from pydantic import BaseModel, Field

# Document Annotation response format
class Product(BaseModel):
    name: str = Field(..., description="The name of the product.")
    description: str = Field(..., description="The description of the product.")
    dimensions: str = Field(..., description="The dimensions of the product.")
    weight: str = Field(..., description="The weight of the product.")
    color: str = Field(..., description="The color of the product.")
    availability: str = Field(..., description="The availability of the product.")
    price: str = Field(..., description="The price of the product.")

class Document(BaseModel):
  title: str = Field(..., description="The title of the document.")
  #names: list[str] = Field(..., description="List of names found in the document.")
  # product in an array of products, each product has a name, description,dimensions, weight, color, availability and a price
  products: list[Product] = Field(..., description="List of products found in the document.")


# Function to encode a local file into data URL 
def local_file_to_data_url(file_path):
    # Guess the MIME type of the file based on the file extension
    mime_type, _ = guess_type(file_path)
    if mime_type is None:
        mime_type = 'application/octet-stream'  # Default MIME type if none is found

    # Read and encode the file
    with open(file_path, "rb") as file:

        base64_encoded_data = base64.b64encode(file.read()).decode('utf-8')

    # Construct the data URL
    return f"data:{mime_type};base64,{base64_encoded_data}"


document_url = local_file_to_data_url(
    '../data/ocr/Products.pdf'
)

mistral_server_url = os.environ["MISTRAL_SERVER_URL"]
api_key = os.environ["MISTRAL_API_KEY"]
model = os.environ.get("MISTRAL_MODEL", "mistral-document-ai-2512")

print(f"Using Mistral server URL: {mistral_server_url}")
print(f"Using Mistral model: {model}")

client = MistralAzure(api_key=api_key, server_url=mistral_server_url)

response = client.ocr.process(
    model=model,
    document={
        "type": "document_url",
        "document_url": document_url
    },
    document_annotation_format={
        "type": "json_schema",
        "json_schema": {
            "name": "Document",
            "schema": Document.model_json_schema(),
            "strict": True
        }
    },
    
#    document_annotation_format=response_format_from_pydantic_model(Document),
    include_image_base64=False
)

#print("Extracted text:")
#print(response)

if response.document_annotation is not None:
    documentParsed = Document.model_validate_json(response.document_annotation)
    #print("Parsed document annotation:")
    #print(documentParsed.model_dump_json(indent=2))
    for product in documentParsed.products:
        print(f"Product Name: {product.name}")
        print(f"Description: {product.description}")
        print(f"Dimensions: {product.dimensions}")
        print(f"Weight: {product.weight}")
        print(f"Color: {product.color}")
        print(f"Availability: {product.availability}")
        print(f"Price: {product.price}")
        print("-" * 40)

#print(response.document_annotation.json(indent=2))

savetheFile = False
if savetheFile:
    # save in a local file 
    filename = "annotated_document.json"
    if os.path.exists(filename):
        #delete the file if it already exists
        os.remove(filename)

    with open(filename, "w", encoding="utf-8") as f:
        f.write(response.document_annotation)