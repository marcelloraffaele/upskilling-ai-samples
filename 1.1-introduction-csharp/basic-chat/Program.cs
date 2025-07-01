// Add Azure OpenAI packages
using Azure.AI.OpenAI;
using DotNetEnv;
using OpenAI.Chat;
using Azure;

// Load environment variables from .env file
Env.Load( );

// Get secrets from .env file
string oaiEndpoint = Environment.GetEnvironmentVariable("AZURE_OPENAI_ENDPOINT")
    ?? throw new InvalidOperationException("AZURE_OPENAI_ENDPOINT environment variable is not set.");
string oaiKey = Environment.GetEnvironmentVariable("AZURE_OPENAI_API_KEY")
    ?? throw new InvalidOperationException("AZURE_OPENAI_API_KEY environment variable is not set.");
string oaiDeploymentName = Environment.GetEnvironmentVariable("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME")
    ?? throw new InvalidOperationException("AZURE_OPENAI_CHAT_DEPLOYMENT_NAME environment variable is not set.");

// Define messages
string systemMessage = "You are a helpful AI assistant.";

// Configure the Azure OpenAI client
AzureOpenAIClient azureClient = new(new Uri(oaiEndpoint), new AzureKeyCredential(oaiKey)); // Use AzureKeyCredential
ChatClient chatClient = azureClient.GetChatClient(oaiDeploymentName);

List<ChatMessage> messageList = new List<ChatMessage>();
messageList.Add(new SystemChatMessage(systemMessage));

while (true)
{



    Console.WriteLine("Please insert your prompt:");
    string userMessage = Console.ReadLine();
    messageList.Add(new UserChatMessage(userMessage));

    ChatCompletionOptions chatCompletionOptions = new ChatCompletionOptions()
    {
        Temperature = 0.7f,
        MaxOutputTokenCount = 800
    };

    ChatCompletion completion = chatClient.CompleteChat(
        messageList,
        chatCompletionOptions
    );

    Console.WriteLine($"{completion.Role}: {completion.Content[0].Text}");

    messageList.Add(new AssistantChatMessage(completion.Content[0].Text));
    Console.WriteLine("Press any key to continue or 'q' to quit.");
    string? key = Console.ReadKey(true).KeyChar.ToString();
    if (key == "q")
    {
        Console.WriteLine("Exiting the application.");
        break;
    }
}



