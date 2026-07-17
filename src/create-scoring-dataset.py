from utils.ai import send, add_user_message, add_assistant_message
import json
import os

prompt = """
Generate an evaluation dataset for a prompt evaluation. The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. Generate an array of JSON objects, each representing task that requires Python, JSON, or a Regex to complete.

Example output:
```json
[
{
    "task": "Description of task",
    "format": "python" | "json" | "regex",
    "solution_criteria": "Key characteristics a good solution has to have."
},
...additional
]
```

* Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single regex
* Focus on tasks that do not require writing much code
* Respond only with Python, JSON, or a plain Regex
* Do not add any comments or commentary or explanation

Please generate 3 objects.
"""

add_user_message(prompt)
add_assistant_message("```code")
response = send({
    "stop_sequences": ["```"],
})
dataset = json.loads(response)
if os.path.exists("dataset-scoring.json"):
    os.remove("dataset-scoring.json")
with open("dataset-scoring.json", "w") as f:
    json.dump(dataset, f, indent=2)
