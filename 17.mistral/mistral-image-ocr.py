import os
from mistralai.azure.client import MistralAzure

import base64
from mimetypes import guess_type

from dotenv import load_dotenv
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


image_url = local_image_to_data_url('../data/images/receipt1.jpg')
print(f"Data URL for the image: {image_url[:100]}...")  #

mistral_server_url = os.environ["MISTRAL_SERVER_URL"]
api_key = os.environ["MISTRAL_API_KEY"]
model = os.environ.get("MISTRAL_MODEL", "mistral-document-ai-2512")

print(f"Using Mistral server URL: {mistral_server_url}")
print(f"Using Mistral model: {model}")

client = MistralAzure(api_key=api_key, server_url=mistral_server_url)

ocr_response = client.ocr.process(
    model=model,
    document={
        "type": "image_url",
        "image_url": image_url
    },
    # table_format=None,
    include_image_base64=True
)

print("Extracted text:")
print(ocr_response)

# save in a local file 
filename = "output.md"
if os.path.exists(filename):
    #delete the file if it already exists
    os.remove(filename)
with open(filename, "w") as f:
    f.write(ocr_response.pages[0].markdown)