import asyncio

from task.clients.client import DialClient
from task.clients.custom_client import CustomDialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role

from dotenv import load_dotenv


async def start(stream: bool) -> None:
   
    # Standard DialClient by default
    dial_client = DialClient(deployment_name="deepseek-r1")
    print("Select client to use: 1. CustomDialClient  2.(or any other symbol(s)) DialClient")
    client_choice = input('>>> ').strip()
    # 1.1. Create DialClient
    if client_choice == '1':
        # 1.2. Create CustomDialClient
        dial_client = CustomDialClient(deployment_name="deepseek-r1")

        
    # (you can get available deployment_name via https://ai-proxy.lab.epam.com/openai/models
    
    #  you can import Postman collection to make a request, file in the project root `dial-basics.postman_collection.json`
    #  don't forget to add your API_KEY)
    
    
    # 2. Create Conversation object
    conversation = Conversation()
    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    print("Enter system prompt or press enter to use default and press 'enter' to continue:")
    system_prompt = input('>>> ').strip()
    if not system_prompt:
        conversation.add_message(
            Message(role=Role.SYSTEM, content=DEFAULT_SYSTEM_PROMPT)
        )
    else:
        conversation.add_message(
            Message(role=Role.SYSTEM, content=system_prompt)
        )
    # 4. Use infinite cycle (while True) and get yser message from console
    
    print("Ask your questions below (type 'exit' to quit):")
    while True:
        user_input = input('You: ').strip()
        # 5. If user message is `exit` then stop the loop
        if user_input.lower() == 'exit':
            print("Exiting the chat. Goodbye!")
            break

        print("AI: ", end=" ", flush=True)


    
    # 6. Add user message to conversation history (role 'user')
        conversation.add_message(
            Message(role=Role.USER, content=user_input)
        )
    # 7. If `stream` param is true -> call DialClient#stream_completion()
    #    else -> call DialClient#get_completion()
        if stream:
            response_message = await dial_client.stream_completion(
                conversation.get_messages()
            )
        else:
            response_message = await dial_client.get_completion(
                conversation.get_messages()
            )
        
    # 8. Add generated message to history
        conversation.add_message(response_message)
    # 9. Test it with DialClient and CustomDialClient
    # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response  
load_dotenv()
asyncio.run(
    start(True)
)
