import os
from dotenv import load_dotenv
from utils.tools_handler import handle_tool_calls
load_dotenv()
from anthropic import Anthropic

if os.path.exists("ai.log"):
    os.remove("ai.log")

client = Anthropic()
model = "claude-sonnet-5"
messages = []

def add_user_message(content):
    user_message = {"role": "user", "content": content}
    messages.append(user_message)

def add_assistant_message(content):
    assistant_message = {"role": "assistant", "content": content}
    messages.append(assistant_message)

def clear_messages():
    messages.clear()

def send(params={}, print_response=False):
    if "model" not in params:
        params["model"] = model
    params["max_tokens"] = 1000
    params["messages"] = messages
    
    with client.messages.stream(**params) as stream:
        if print_response:
            for text in stream.text_stream:
                print(text, end="")
        final_message = stream.get_final_message()

    text_parts = []
    tool_uses = []
    for block in final_message.content:
        if block.type == "text":
            text_parts.append(block.text)
        elif block.type == "tool_use":
            tool_uses.append({
                "id": block.id,
                "name": block.name,
                "input": block.input
            })
        elif block.type == "max_tokens":
            exit("Max tokens limit reached.")
    
    with open("ai.log", "a") as f:
        if text_parts:
            f.write("\n".join(text_parts).strip() + "\n")
        if tool_uses:
            f.write(f"Tool calls: {tool_uses}\n")
        f.write("-"*40 + "\n")
    
    if tool_uses:
        assistant_messages, tool_messages = handle_tool_calls(tool_uses)
        add_assistant_message(assistant_messages)
        add_user_message(tool_messages)
        tool_result = send(params, print_response)
        text_parts.append(tool_result)
    
    return "\n".join(text_parts).strip()
