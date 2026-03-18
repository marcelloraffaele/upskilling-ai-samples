# https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/openapi-spec-samples?pivots=python
import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
# import the folloing 
from azure.ai.agents.models import OpenApiTool, OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme
from azure.ai.projects.models import PromptAgentDefinition

from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()


# Retrieve the project endpoint from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]
model_name = os.environ["MODEL_DEPLOYMENT_NAME"]
agentName = "todo-openapi-agent"

# Create an AIProjectClient instance
project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()  # Use Azure Default Credential for authentication
)

with project_client:

    # Load the OpenAPI specification for the todo app from a local JSON file
    with open(os.path.join(os.path.dirname(__file__), "todo-app-API-definition.json"), "r") as f:
         openapi_todo = jsonref.loads(f.read())

    # Create Auth object for the OpenApiTool (note: using anonymous auth here; connection or managed identity requires additional setup)
    #auth = OpenApiAnonymousAuthDetails()
    # for connection setup
    auth = OpenApiConnectionAuthDetails(security_scheme=OpenApiConnectionSecurityScheme(connection_id=os.environ["TODO_APP_CONN_ID"]))
    # for managed identity set up
    # auth = OpenApiManagedAuthDetails(security_scheme=OpenApiManagedSecurityScheme(audience="https://your_identity_scope.com"))

    # Initialize the main OpenAPI tool definition for todo
    openapi_tool = OpenApiTool(
        name="get_todo", spec=openapi_todo, description="Retrieve todo information", auth=auth
    )

    agent = None
#    try:
#        # Check if the agent already exists
#        agentDetails = project_client.agents.get(agentName)
#        if agentDetails is not None and agentDetails.versions is not None:
#            version = agentDetails.versions.latest.version
#            agent = project_client.agents.get_version(agentName, version)
#    except Exception as e:
#        agent = None

    if agent is None:
        agent = project_client.agents.create_version(
            agent_name=agentName,
            definition=PromptAgentDefinition(
                model=os.environ["MODEL_DEPLOYMENT_NAME"],
                instructions="You are a helpful agent",
                tools=openapi_tool.definitions
            ),
        )    

    openai_client = project_client.get_openai_client()

    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    while True:
        user_input = input("Enter a command for your api (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        openai_client.conversations.items.create(
            conversation_id=conversation.id,
            items=[{"type": "message", "role": "user", "content": user_input}],
        )

        response = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent_reference": {"name": agent.name, "version": agent.version, "type": "agent_reference"}},
        )

        print(f"output: {response.output_text}")

    openai_client.conversations.delete(conversation.id)
    print("Deleted conversation")
    
    # Delete the agent after use
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")