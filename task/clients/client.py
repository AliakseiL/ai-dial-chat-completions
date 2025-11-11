from aidial_client import Dial, AsyncDial

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self._client = Dial(
            api_key=self._api_key,
            base_url=DIAL_ENDPOINT
        )
        self._async_client = AsyncDial(
            api_key=self._api_key,
            base_url=DIAL_ENDPOINT
        )

    def get_completion(self, messages: list[Message]) -> Message:
        response = self._client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=[msg.to_dict() for msg in messages]
        )
        if not response.choices:
            raise Exception("No choices in response found")
        content = response.choices[0].message.content
        return Message(role=Role.AI, content=content)

    async def stream_completion(self, messages: list[Message]) -> Message:
        chunks = await self._async_client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=[msg.to_dict() for msg in messages],
            stream=True
        )
        contents = []
        async for chunk in chunks:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    content_chunk = delta.content
                    print(content_chunk, end="", flush=True)
                    contents.append(content_chunk)
        print()
        full_content = "".join(contents)
        return Message(role=Role.AI, content=full_content)
