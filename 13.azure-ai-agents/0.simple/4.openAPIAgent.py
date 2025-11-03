# https://learn.microsoft.com/en-us/azure/ai-foundry/agents/how-to/tools/openapi-spec-samples?pivots=python
import os
import jsonref
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
# import the folloing 
from azure.ai.agents.models import OpenApiTool, OpenApiConnectionAuthDetails, OpenApiConnectionSecurityScheme

from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()


# Retrieve the project endpoint from environment variables
project_endpoint = os.environ["PROJECT_ENDPOINT"]
model_name = os.environ["MODEL_DEPLOYMENT_NAME"]


with AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential()
) as project_client:
    agents_client = project_client.agents

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

    # Create an agent and run user's request with function calls
    agent = agents_client.create_agent(
        model=os.environ["MODEL_DEPLOYMENT_NAME"],
        name="todo-openapi-agent",
        instructions="You are a helpful agent",
        tools=openapi_tool.definitions
    )
    print(f"Created agent, ID: {agent.id}")

    thread = agents_client.threads.create()
    print(f"Created thread, ID: {thread.id}")

    while True:
        user_input = input("Enter a command for your api (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        message = agents_client.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_input
        )
        print(f"Created message, ID: {message.id}")

        # Create and automatically process the run, handling tool calls internally
        run = project_client.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)
        print(f"Run finished with status: {run.status}")

        if run.status == "failed":
            print(f"Run failed: {run.last_error}")
            break

        # Retrieve the steps taken during the run for analysis
        run_steps = project_client.agents.run_steps.list(thread_id=thread.id, run_id=run.id)

        # Loop through each step to display information
        for step in run_steps:
            print(f"Step {step['id']} status: {step['status']}")

            tool_calls = step.get("step_details", {}).get("tool_calls", [])
            for call in tool_calls:
                print(f"  Tool Call ID: {call.get('id')}")
                print(f"  Type: {call.get('type')}")
                function_details = call.get("function", {})
                if function_details:
                    print(f"  Function name: {function_details.get('name')}")
                    print(f" function output: {function_details.get('output')}")

            print()

        # Fetch and log all messages
        #messages = project_client.agents.messages.list(thread_id=thread.id)
        #for message in messages:
        #    print(f"Role: {message.role}, Content: {message.content}")
        answer = project_client.agents.messages.get_last_message_by_role(thread_id=thread.id, role="assistant")
        print(f"answer from assistant: {answer.content[0].text.value}")

    # Delete the agent after use
    project_client.agents.delete_agent(agent.id)
    print("Deleted agent")