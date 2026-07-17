from utils.ai import send, add_user_message
from tools.get_current_datetime import get_current_datetime_schema
from tools.add_duration_to_datetime import add_duration_to_datetime_schema

add_user_message("Can you tell me the date after 103 days from now?");
response = send({
    "tools": [get_current_datetime_schema, add_duration_to_datetime_schema],
})
print(response)
