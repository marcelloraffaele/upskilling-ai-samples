# pip install azure-ai-inference
import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

endpoint = os.getenv("DEEPSEEK_ENDPOINT") 
api_key = os.getenv("DEEPSEEK_API_KEY", '')
if not api_key:
  raise Exception("A key should be provided to invoke the endpoint")

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api_key)
)

model_info = client.get_model_info()
print("Model name:", model_info.model_name)
print("Model type:", model_info.model_type)
print("Model provider name:", model_info.model_provider_name)

messages = [
    {
        "role": "system",
        "content": "You are an AI agent that work at `Sport House` shoes shop." + 
                    "You can answer only to the following FAQ:\n" +
                    "1. What types of sport shoes do you offer? At Sport House, we offer a wide range of sport shoes including running shoes, basketball shoes, soccer cleats, tennis shoes, and more. Our collection caters to athletes of all levels and sports enthusiasts.\n\n" +
                    "2. How do I find the right size? We recommend using our size guide, which is available on each product page. Measure your foot and compare it to the size chart to find the perfect fit. If you're unsure, our customer service team is here to help.\n\n" +
                    "3. What is your return policy? We offer a 30-day return policy for unworn sport shoes in their original packaging. If you need to return or exchange an item, please contact our customer service team for assistance.\n\n" +
                    "4. How can I track my order? Once your order is shipped, you will receive a tracking number via email. You can use this number to track your order on our website.\n\n" +
                    "5. Do you offer international shipping? Yes, we offer international shipping to many countries. Shipping fees and delivery times vary depending on the destination.\n\n" +
                    "6. What payment methods do you accept? We accept various payment methods including credit/debit cards, PayPal, and other secure payment options.\n\n" + 
                    "7. How can I contact customer service? You can reach our customer service team via email at support@sporthouse.com or by calling our toll-free number at 1-800-123-4567.\n\n" + 
                    "8. Are there any ongoing promotions or discounts? Yes, we frequently offer promotions and discounts. Please check our website or subscribe to our newsletter to stay updated on the latest deals."
    }
]


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

    payload = {
    "messages": messages,
    "max_tokens": 2048
    }
    response = client.complete(payload)

    print("AI: ", response.choices[0].message.content)
    #print("Model:", response.model)
    #print("Usage:")
    #print("	Prompt tokens:", response.usage.prompt_tokens)
    #print("	Total tokens:", response.usage.total_tokens)
    #print("	Completion tokens:", response.usage.completion_tokens)
    messages.append({
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": response.choices[0].message.content
            }
        ]
    })