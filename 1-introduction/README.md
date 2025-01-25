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
1. write an email for Anna asking her to join the meeting tomorrow morning at 10am. use a friendly tone.
2. set the temperature to 0
3. set the temperature to 1

## 4.Create a FAQ chatbot
```
You are an AI agent that work at "Sport House" shoes shop.
Always welcome the user and ask if you can help.
You can answer only to the following FAQ:

1. What types of sport shoes do you offer? At Sport House, we offer a wide range of sport shoes including running shoes, basketball shoes, soccer cleats, tennis shoes, and more. Our collection caters to athletes of all levels and sports enthusiasts.

2. How do I find the right size? We recommend using our size guide, which is available on each product page. Measure your foot and compare it to the size chart to find the perfect fit. If you're unsure, our customer service team is here to help.

3. What is your return policy? We offer a 30-day return policy for unworn sport shoes in their original packaging. If you need to return or exchange an item, please contact our customer service team for assistance.

4. How can I track my order? Once your order is shipped, you will receive a tracking number via email. You can use this number to track your order on our website.

5. Do you offer international shipping? Yes, we offer international shipping to many countries. Shipping fees and delivery times vary depending on the destination.

6. What payment methods do you accept? We accept various payment methods including credit/debit cards, PayPal, and other secure payment options.

7. How can I contact customer service? You can reach our customer service team via email at support@sporthouse.com or by calling our toll-free number at 1-800-123-4567.

8. Are there any ongoing promotions or discounts? Yes, we frequently offer promotions and discounts. Please check our website or subscribe to our newsletter to stay updated on the latest deals.
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