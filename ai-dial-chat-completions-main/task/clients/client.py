import os
from aidial_client import Dial, AsyncDial

from dotenv import load_dotenv
from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class DialClient(BaseClient):

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)        
        self.api_key = os.getenv("DIAL_API_KEY", "")
        self.base_url = os.getenv("DIAL_API_BASE", "")
        
        # Documentation: https://pypi.org/project/aidial-client/ (here you can find how to create and use these clients)
        # 1. Create Dial client
        self._client = Dial(api_key=self.api_key, base_url=self.base_url)
        
        # 2. Create AsyncDial client
        self._async_client = AsyncDial(api_key=self.api_key, base_url=self.base_url)
        self.client = self._client
        self.async_client = self._async_client

    def get_completion(self, messages: list[Message]) -> Message:        
        # 1. Create chat completions with client
        response = self._client.chat.completions.create(
            deployment_name=self._deployment_name,
            stream=False,
            messages=[message.to_dict() for message in messages]
        )
        #    Hint: to unpack messages you can use the `to_dict()` method from Message object
        # 2. Get content from response, print it and return message with assistant role and content
        # 3. If choices are not present then raise Exception("No choices in response found")
        if choices := response.choices:            
            if message := choices[0].message:
                print(message.content)            
                return Message(role=Role.AI, content=message.content)

    async def stream_completion(self, messages: list[Message]) -> Message:
       
        # 1. Create chat completions with async client
        #    Hint: don't forget to add `stream=True` in call.
        
        chunks_response = await self._async_client.chat.completions.create(
            deployment_name=self._deployment_name,
            stream=True,
            messages=[message.to_dict() for message in messages]
        )
        # 2. Create array with `contents` name (here we will collect all content chunks)
        contents = []
        # 3. Make async loop from `chunks` (from 1st step)
        async for chunk in chunks_response:
           
            if chunk.choices:
                content_chunk = chunk.choices[0].delta.content
                if content_chunk:
                    # 4 Print content chunk without new line in the end
                    print(content_chunk, end="", flush=True)
                    # 4.1 Append content chunk to `contents` array
                    contents.append(content_chunk)
        
        # 5. Print empty row `print()` (it will represent the end of streaming and in console we will print input from a new line)
        print()
        # 6. Return Message with assistant role and message collected content
        return Message(role=Role.AI, content="".join(contents))