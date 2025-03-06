# Azure AI Foundry

(Azure AI Foundry)[https://ai.azure.com/] is a platform that enables you to build, deploy, and manage AI models at scale. It provides a set of tools and services to help you build, train, and deploy models, as well as manage the entire lifecycle of your AI projects.

The first step is to create a new project in Azure AI Foundry.

Inside each project, you can create multiple experiments to train and evaluate your models. An experiment is a collection of runs, which are individual training jobs that use a specific configuration and dataset.
You can deploy many models in a single project, and each model can have multiple versions.

Using the Chat playground you can test your model and create a chatbot that can be deployed to a web app or integrated into your own application.

## 1. Show project and how to create a new project

1. Go to the Azure AI Foundry portal: https://ai.azure.com/
2. Click on the "Projects" tab on the left sidebar
3. Click on the "Create project" button
4. Enter a name for your project and click "Create"


## 2. Simple chat
Reset the system message and ask the following questions:
1. what's your last update?
2. what time is in london now ?
3. what is the weather in london ?
4. what is prompt engineering?

## 3. Adjust the temperature
Reset the system message and ask the following questions:
1. I have a red cat can you help me to choose a name?
2. set the temperature to 0
3. set the temperature to 1

## 4.Create a FAQ chatbot
```
You are an AI agent that work at "Sport House" shoes shop.
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
Let me know if you need any more information!
```

Questions: 
what product do you sell ?
how do I find the right size ?
if a buy a product can i change it ?

## 5. Deploy the chat app
1. Click on the "Deploy" button
2. Select the "Web app" option
3. Click on the "Deploy" button
4. Click on the "View app" button to test the chatbot


## 6. Understanding the Rest API
1. Click on 'view code' and choose "curl"
2. Copy the curl or go to the file 

## 7. Create a Python script to interact with OpenAI
1. From the AI Foundry, click on 'view code' and choose "Python"
2. Select 'Key based authentication' and copy the code or open the 3.completion.py file
3. After you can see also the code for 4.faq-chat.py

## 8. Create a Jupiter notebook to interact with OpenAI
1. From the AI Foundry, click on 'view code' and choose "Python" or open the 5.faq-notebook.ipynb file


### resources
- https://learn.microsoft.com/en-us/azure/ai-services/openai/reference