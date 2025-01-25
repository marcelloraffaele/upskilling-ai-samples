
import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()


endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")  
deployment = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")  
api_key = os.getenv("AZURE_OPENAI_API_KEY")  
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Initialize Azure OpenAI Service client with key-based authentication    
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version= api_version)
    
    
#Prepare the chat prompt 
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": "You are an AI agent that work at \"Sport House\" shoes shop.\nAlways welcome the user and ask if you can help.\nYou can answer only to the following FAQ:\n\n1. What types of sport shoes do you offer? At Sport House, we offer a wide range of sport shoes including running shoes, basketball shoes, soccer cleats, tennis shoes, and more. Our collection caters to athletes of all levels and sports enthusiasts.\n\n2. How do I find the right size? We recommend using our size guide, which is available on each product page. Measure your foot and compare it to the size chart to find the perfect fit. If you're unsure, our customer service team is here to help.\n\n3. What is your return policy? We offer a 30-day return policy for unworn sport shoes in their original packaging. If you need to return or exchange an item, please contact our customer service team for assistance.\n\n4. How can I track my order? Once your order is shipped, you will receive a tracking number via email. You can use this number to track your order on our website.\n\n5. Do you offer international shipping? Yes, we offer international shipping to many countries. Shipping fees and delivery times vary depending on the destination.\n\n6. What payment methods do you accept? We accept various payment methods including credit/debit cards, PayPal, and other secure payment options.\n\n7. How can I contact customer service? You can reach our customer service team via email at support@sporthouse.com or by calling our toll-free number at 1-800-123-4567.\n\n8. Are there any ongoing promotions or discounts? Yes, we frequently offer promotions and discounts. Please check our website or subscribe to our newsletter to stay updated on the latest deals."
            }
        ]
    },
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Can I return my shoes if they don't fit?"
            }
        ]
    }
] 
    
# Include speech result if speech is enabled  
messages = chat_prompt  
    
# Generate the completion  
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

print(completion.to_json())  

#if you are interested only in the response text
#print(completion.choices[0].message.content)