from utils.ai import send, add_user_message, add_assistant_message
import json
import os

prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate meal plans for athletes. Generate an array of JSON objects, each representing a task that requires a meal plan to complete.

Example output:
```json
[
{
    "task": "Description of task",
    "height": "Athlete's height in cm",
    "weight": "Athlete's weight in kg", 
    "goal": "Goal of the athlete",
    "restrictions": "Dietary restrictions of the athlete"
},
...additional
]
```

Please generate 3 objects.
"""

add_user_message(prompt)
add_assistant_message("```json")
response = send({
    "stop_sequences": ["```"],
}, print_response=False)
dataset = json.loads(response)
if os.path.exists("dataset-mealplan.json"):
    os.remove("dataset-mealplan.json")
with open("dataset-mealplan.json", "w") as f:
    json.dump(dataset, f, indent=2)
