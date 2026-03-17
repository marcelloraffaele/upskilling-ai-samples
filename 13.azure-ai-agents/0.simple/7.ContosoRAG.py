# Before running the sample:
#    pip install --pre azure-ai-projects>=2.0.0b4

import os

from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_endpoint = os.environ["PROJECT_ENDPOINT"]

project_client = AIProjectClient(
    endpoint=project_endpoint,
    credential=DefaultAzureCredential(),
)

my_agent = "ContosoElectronicsRAG"
my_version = "3"

openai_client = project_client.get_openai_client()

# Reference the agent to get a response
response = openai_client.responses.create(
    input=[{"role": "user", "content": "Which is the price of the employee health plan?."}],
    extra_body={"agent_reference": {"name": my_agent, "version": my_version, "type": "agent_reference"}},
)

print(f"Response output: {response.output_text}")



