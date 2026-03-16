import os
import asyncio
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

async def basic_foundry_mcp_example():
    """Basic example of Azure AI Foundry agent with hosted MCP tools."""
    async with (
        DefaultAzureCredential() as credential,
        AzureAIAgentClient(
            project_endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
            model_deployment_name=os.environ["MODEL_DEPLOYMENT_NAME"],
            async_credential=credential) as client,
    ):
        # Create a hosted MCP tool using the client method
        learn_mcp = client.get_mcp_tool(
            name="Microsoft Learn MCP",
            url="https://learn.microsoft.com/api/mcp",
        )

        # Create agent with hosted MCP tool
        agent = client.as_agent(
            name="MicrosoftLearnAgent", 
            instructions="You answer questions by searching Microsoft Learn content only.",
            tools=[learn_mcp],
        )

        # Simple query without approval workflow
        result = await agent.run(
            "Please summarize the Azure AI Agent documentation related to MCP tool calling?"
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(basic_foundry_mcp_example())