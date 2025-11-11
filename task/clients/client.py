from aidial_client import Dial, AsyncDial

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        #TODO:
        # Documentation: https://pypi.org/project/aidial-client/ (here you can find how to create and use these clients)
        # 1. Create Dial client
        # 2. Create AsyncDial client
        self._client = Dial(
            api_key=self._api_key,
            base_url=DIAL_ENDPOINT
        )
        self._async_client = AsyncDial(
            api_key=self._api_key,
            base_url=DIAL_ENDPOINT
        )

    def get_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # 1. Create chat completions with client
        #    Hint: to unpack messages you can use the `to_dict()` method from Message object
        # 2. Get content from response, print it and return message with assistant role and content
        # 3. If choices are not present then raise Exception("No choices in response found")
        response = self._client.chat.completions.create(
            deployment_name=self._deployment_name,
            messages=[msg.to_dict() for msg in messages]
        )
        if not response.choices:
            raise Exception("No choices in response found")
        content = response.choices[0].message.content
        return Message(role=Role.AI, content=content)

    async def stream_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # 1. Create chat completions with async client
        #    Hint: don't forget to add `stream=True` in call.
        # 2. Create array with `contents` name (here we will collect all content chunks)
        # 3. Make async loop from `chunks` (from 1st step)
        # 4. Print content chunk and collect it contents array
        # 5. Print empty row `print()` (it will represent the end of streaming and in console we will print input from a new line)
        # 6. Return Message with assistant role and message collected content
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
