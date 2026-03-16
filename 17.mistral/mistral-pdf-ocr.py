import os
from mistralai.azure.client import MistralAzure

import base64
from mimetypes import guess_type

from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()



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


document_url = local_file_to_data_url('../data/ocr/example1.pdf')

mistral_server_url = os.environ["MISTRAL_SERVER_URL"]
api_key = os.environ["MISTRAL_API_KEY"]
model = os.environ.get("MISTRAL_MODEL", "mistral-document-ai-2512")

print(f"Using Mistral server URL: {mistral_server_url}")
print(f"Using Mistral model: {model}")

client = MistralAzure(api_key=api_key, server_url=mistral_server_url)

ocr_response = client.ocr.process(
    model=model,
    document={
        "type": "document_url",
        "document_url": document_url
    },
    # table_format=None,
    include_image_base64=True
)

#print("Extracted text:")
#print(ocr_response)

# save in a local file 
filename = "output.md"
if os.path.exists(filename):
    #delete the file if it already exists
    os.remove(filename)

with open(filename, "w", encoding="utf-8") as f:
    for page in ocr_response.pages:
        f.write(page.markdown)