import os
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.agents.models import CodeInterpreterTool
from azure.ai.projects.models import PromptAgentDefinition
import jsonref
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

# Create an AIProjectClient from an endpoint, copied from your Azure AI Foundry project.
# You need to login to Azure subscription via Azure CLI and set the environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]  # Ensure the PROJECT_ENDPOINT environment variable is set

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),  # Use Azure Default Credential for authentication
)

code_interpreter = CodeInterpreterTool()
with project_client:

    agentName = "math-agent"

    agent = None
    try:
        # Check if the agent already exists
        agentDetails = project_client.agents.get(agentName)
        if agentDetails is not None and agentDetails.versions is not None:
            version = agentDetails.versions.latest.version
            agent = project_client.agents.get_version(agentName, version)
    except Exception as e:
        agent = None

    if agent is None:
        agent = project_client.agents.create_version(
            agent_name=agentName,
            definition=PromptAgentDefinition(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                instructions="You politely help with math questions. Use the Code Interpreter tool when asked to visualize numbers.",  # Instructions for the agent
                tools=code_interpreter.definitions,  # Attach the tool
            ),
        )

    print(f"Agent {agentName} already exists, ID: {agent.id}, version: {agent.version}")

    openai_client = project_client.get_openai_client()

    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{
            "type": "message", 
            "role": "user", 
            "content": "Hi, Agent! Draw a graph for a line with a slope of 4 and y-intercept of 9."
        }],
    )


    response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "version": agent.version, "type": "agent_reference"}},
        )

    #print( jsonref.dumps(response.to_dict(), indent=2) )

    print(f"Output: {response.output_text}")

    # Print code executed by the code interpreter tool.
    # [START code_output_extraction]
    code = next((output.code for output in response.output if output.type == "code_interpreter_call"), "")
    print(f"Code Interpreter code:")
    print(code)
    # [END code_output_extraction]
    
    # Uncomment these lines to delete the agent when done
    # agents_client.delete_agent(agent.id)
    # print("Deleted agent")