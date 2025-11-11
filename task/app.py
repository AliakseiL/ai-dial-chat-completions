import asyncio

from task.clients.client import DialClient
from task.clients.custom_client import CustomDialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:

    dial_client = DialClient(deployment_name = "gpt-5-mini-2025-08-07")

    custom_dial_client = CustomDialClient(deployment_name="gpt-5-mini-2025-08-07")

    conversation = Conversation()

    system_prompt = input("Enter system prompt (press Enter for default): ").strip()
    if not system_prompt:
        system_prompt = DEFAULT_SYSTEM_PROMPT
        print("Using default system prompt.")
    conversation.add_message(Message(role=Role.SYSTEM, content=system_prompt))

    print("Enter your question (type `exit` to quit):")
    while True:
        user_input = input("> ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        conversation.add_message(Message(role=Role.USER, content=user_input))

        if stream:
            ai_message = await custom_dial_client.stream_completion(conversation.messages)
        else:
            ai_message = custom_dial_client.get_completion(conversation.messages)

        conversation.add_message(ai_message)
        print(f"AI: {ai_message.content}")


asyncio.run(
    start(True)
)
