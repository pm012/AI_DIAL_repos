import json
import os
import aiohttp
import requests

#from dotenv import load_dotenv
from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role


class CustomDialClient(BaseClient):
    _endpoint: str
    _api_key: str

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self._api_key = os.getenv("DIAL_API_KEY", "")
        self._base_url = os.getenv("DIAL_API_BASE", "")
        self._endpoint = self._base_url + f"/openai/deployments/{deployment_name}/chat/completions"

    def get_completion(self, messages: list[Message]) -> Message:
       
        # Take a look at README.md of how the request and regular response are looks like!
        # 1. Create headers dict with api-key and Content-Type
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }
        # 2. Create request_data dictionary with:
        #   - "messages": convert messages list to dict format using msg.to_dict() for each message
        request_data = {
            "messages": [message.to_dict() for message in messages]
        }
        # 3. Make POST request using requests.post() with:
        #   - URL: self._endpoint
        #   - headers: headers from step 1
        #   - json: request_data from step 2
        response = requests.post(
            url=self._endpoint,
            headers=headers,
            json=request_data
        )
        # 4. Get content from response, print it and return message with assistant role and content
        if response.status_code == 200:
            response_data = response.json()
            if choices := response_data.get("choices", []):
                content = choices[0].get("message",{}).get("content")                    
                print(content)
                return Message(role=Role.AI, content=content)
        # 5. If status code != 200 then raise Exception with format: f"HTTP {response.status_code}: {response.text}"
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")

    async def stream_completion(self, messages: list[Message]) -> Message:
        
        # Take a look at README.md of how the request and streamed response chunks are looks like!
        # 1. Create headers dict with api-key and Content-Type
        headers = {
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }
        # 2. Create request_data dictionary with:
        #    - "stream": True  (enable streaming)
        #    - "messages": convert messages list to dict format using msg.to_dict() for each message
        request_data = {
            "stream": True,
            "messages": [message.to_dict() for message in messages]
        }
        # 3. Create empty list called 'contents' to store content snippets
        contents = []
        # 4. Create aiohttp.ClientSession() using 'async with' context manager
        async with aiohttp.ClientSession() as session:
             # 5. Inside session, make POST request using session.post() with:
        #    - URL: self._endpoint
        #    - json: request_data from step 2
        #    - headers: headers from step 1
        #    - Use 'async with' context manager for response
            async with session.post(url=self._endpoint, headers=headers, json=request_data) as response:
                if response.status == 200:
                    # 6. Get content from chunks (don't forget that chunk start with `data: `, final chunk is `data: [DONE]`), print
                    #    chunks, collect them and return as assistant message
                    async for line in response.content:
                        line_str = line.decode('utf-8').strip()
                        if line_str.startswith("data: "):
                            data = line_str[6:].strip()
                            if data != "[DONE]":
                                content_snippet = self._get_content_snippet(data)
                                if content_snippet:  # Only append non-empty strings
                                    print(content_snippet, end='')
                                    contents.append(content_snippet)
                            else:
                                print()                    
                else:
                    error_text = await response.text()
                    print(f"{response.status} {error_text}")
                return Message(role=Role.AI, content=''.join(contents))              
       
    def _get_content_snippet(self, data: str) -> str:
        """Helper method to extract content snippet from chunk data."""
        try:
            chunk = json.loads(data)
            if 'choices' in chunk and len(chunk['choices']) > 0:
                delta = chunk['choices'][0].get('delta', {})
                return delta.get('content', '')
        except json.JSONDecodeError:
            pass
        return ""
    

    