# from docs https://learn.microsoft.com/en-us/azure/ai-services/openai/realtime-audio-quickstart?tabs=api-key%2Cwindows&pivots=programming-language-python
import os
import base64
import asyncio
from azure.core.credentials import AzureKeyCredential
from rtclient import (
    ResponseCreateMessage,
    #RTLowLevelClient,
    ResponseCreateParams
)
from client_extended import RTLowLevelClientExtended

from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Set environment variables or edit the corresponding values here.
api_key = os.environ["AZURE_OPENAI_API_KEY"]    
endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
api_version = os.environ["AZURE_OPENAI_REALTIME_API_VERSION"]
deployment = "gpt-4o-mini-realtime-preview"

async def text_in_audio_out():
    async with RTLowLevelClientExtended(
        url=endpoint,
        azure_deployment=deployment,
        key_credential=AzureKeyCredential(api_key),
        api_version=api_version
    ) as client:
        await client.send(
            ResponseCreateMessage(
                response=ResponseCreateParams(
                    modalities={"audio", "text"}, 
                    instructions="Please assist the user."
                )
            )
        )
        done = False
        while not done:
            message = await client.recv()
            match message.type:
                case "response.done":
                    done = True
                case "error":
                    done = True
                    print(message.error)
                case "response.audio_transcript.delta":
                    print(f"Received text delta: {message.delta}")
                case "response.audio.delta":
                    buffer = base64.b64decode(message.delta)
                    print(f"Received {len(buffer)} bytes of audio data.")
                case _:
                    pass

async def main():
    await text_in_audio_out()

asyncio.run(main())