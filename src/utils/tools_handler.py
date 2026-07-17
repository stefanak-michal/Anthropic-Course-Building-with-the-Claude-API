from tools.get_current_datetime import get_current_datetime
from tools.add_duration_to_datetime import add_duration_to_datetime
from tools.set_reminder import set_reminder

def handle_tool_calls(tool_uses):
    assistant_messages = []
    tool_messages = []
    for tool_use in tool_uses:
        result = None
        if tool_use["name"] == "get_current_datetime":
            if tool_use["input"] and "date_format" in tool_use["input"]:
                date_format = tool_use["input"]["date_format"]
                result = get_current_datetime(date_format)
            else:
                result = get_current_datetime()
        elif tool_use["name"] == "add_duration_to_datetime":
            args = {
                "datetime_str": tool_use["input"]["datetime_str"]
            }
            if "duration" in tool_use["input"]:
                args["duration"] = tool_use["input"]["duration"]
            if "unit" in tool_use["input"]:
                args["unit"] = tool_use["input"]["unit"]
            if "input_format" in tool_use["input"]:
                args["input_format"] = tool_use["input"]["input_format"]
            result = add_duration_to_datetime(**args)
        elif tool_use["name"] == "set_reminder":
            result = set_reminder(tool_use["input"]["content"], tool_use["input"]["timestamp"])
        
        if result:
            assistant_messages.append({
                "type": "tool_use",
                "id": tool_use["id"],
                "name": tool_use["name"],
                "input": tool_use["input"]
            })

            tool_messages.append({
                "type": "tool_result",
                "tool_use_id": tool_use["id"],
                "content": result,
                "is_error": False
            })

    return assistant_messages, tool_messages
