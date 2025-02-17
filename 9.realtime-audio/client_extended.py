# this file is an override of the RTLowLevelClient class from the rtclient module
# I have override :
# - the __init__ method to add the api version and deployment parameters
# - connect method to add the api version and deployment parameters

from rtclient import (
    RTLowLevelClient,
)
from typing import Optional
import uuid
from rtclient.models import ServerMessageType, UserMessageType, create_message_from_dict
from rtclient.util.user_agent import get_user_agent
from aiohttp import ClientSession, WSMsgType, WSServerHandshakeError
from azure.core.credentials import AzureKeyCredential
from azure.core.credentials_async import AsyncTokenCredential


class RTLowLevelClientExtended(RTLowLevelClient):

    def __init__(
        self,
        url: Optional[str] = None,
        token_credential: Optional[AsyncTokenCredential] = None,
        key_credential: Optional[AzureKeyCredential] = None,
        model: Optional[str] = None,
        azure_deployment: Optional[str] = None,
        api_version: Optional[str] = None
    ):
        self._is_azure_openai = url is not None
        if self._is_azure_openai:
            if key_credential is None and token_credential is None:
                raise ValueError("key_credential or token_credential is required for Azure OpenAI")
            if azure_deployment is None:
                raise ValueError("azure_deployment is required for Azure OpenAI")
        else:
            if key_credential is None:
                raise ValueError("key_credential is required for OpenAI")
            if model is None:
                raise ValueError("model is required for OpenAI")

        self._url = url if self._is_azure_openai else "wss://api.openai.com"
        self._token_credential = token_credential
        self._key_credential = key_credential
        self._session = ClientSession(base_url=self._url)
        self._model = model
        self._azure_deployment = azure_deployment
        self._api_version = api_version
        self.request_id: Optional[uuid.UUID] = None
    
    async def connect(self):
        try:
            self.request_id = uuid.uuid4()
            if self._is_azure_openai:
                api_version = self._api_version
                path = "/openai/realtime"
                auth_headers = await self._get_auth()
                headers = {
                    "x-ms-client-request-id": str(self.request_id),
                    "User-Agent": get_user_agent(),
                    **auth_headers,
                }
                self.ws = await self._session.ws_connect(
                    path,
                    headers=headers,
                    params={"deployment": self._azure_deployment, "api-version": api_version},
                )
            else:
                headers = {
                    "Authorization": f"Bearer {self._key_credential.key}",
                    "openai-beta": "realtime=v1",
                    "User-Agent": get_user_agent(),
                }
                self.ws = await self._session.ws_connect("/v1/realtime", headers=headers, params={"model": self._model})
        except WSServerHandshakeError as e:
            await self._session.close()
            error_message = f"Received status code {e.status} from the server"
            raise ConnectionError(error_message, e.headers) from e