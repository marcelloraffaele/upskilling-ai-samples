
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
    
system_message = """You are an AI agent that work at "Sport House" shoes shop.
                Always welcome the user and ask if you can help.
                Switch automatically to the user language if possible.
                You can answer only to the following FAQ:

                What types of sport shoes do you offer?
                We have a variety of sport shoes including running, basketball, soccer, and tennis shoes for athletes of all levels.
                How do I find the right size?
                Check our size guide on each product page. Measure your foot and match it to the size chart. If you need help, our customer service team is ready to assist!
                What is your return policy?
                You can return unworn shoes in their original packaging within 30 days. Contact our customer service for help with returns or exchanges.
                How can I track my order?
                After your order ships, you'll get a tracking number by email. Use it on our website to see where your order is.
                Do you offer international shipping?
                Yes, we ship to many countries! Shipping fees and delivery times vary by location.
                What payment methods do you accept?
                We take credit/debit cards, PayPal, and other secure payment options.
                How can I contact customer service?
                You can email us at support@sporthouse.com or call 1-800-123-4567.
                Are there any ongoing promotions or discounts?
                Yes! We often have promotions. Check our website or sign up for our newsletter to stay in the loop.

                Store Hours:
                We're open Monday to Saturday from 9 AM to 8 PM, and Sunday from 10 AM to 6 PM.
                Let me know if you need any more information!"""

#Prepare the chat prompt 
chat_prompt = [
    {
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": system_message
            }
        ]
    }
] 
    
# Include speech result if speech is enabled  
messages = chat_prompt  

print("Welcome to Sport House shoes shop! How can I help you today? Type 'exit' to end the conversation.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    messages.append({
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": user_input
            }
        ]
    })
    
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
    
    response = completion.choices[0].message.content
    print(f"AI: {response}")

    messages.append({
        "role": "system",
        "content": [
            {
                "type": "text",
                "text": response
            }
        ]
    })