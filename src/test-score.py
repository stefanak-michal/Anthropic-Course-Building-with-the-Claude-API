import re
import ast
from utils.ai import send, add_user_message, add_assistant_message, clear_messages
import json
from statistics import mean
import os

if not os.path.exists("dataset-scoring.json"):
    exit("Dataset file 'dataset-scoring.json' not found. Please run create-scoring-dataset.py first.")

def grade_by_model(test_case, output):
    # Create evaluation prompt
    eval_prompt = f"""
You are an expert code reviewer. Evaluate this AI-generated solution.

<task>
{test_case["task"]}
</task>
<solution>
{output}
</solution>
<criteria>
{test_case["solution_criteria"]}
</criteria>

Provide your evaluation as a structured JSON object with:
- "strengths": An array of 1-3 key strengths
- "weaknesses": An array of 1-3 key areas for improvement  
- "reasoning": A concise explanation of your assessment
- "score": A number between 1-10
    """
    
    clear_messages()
    add_user_message(eval_prompt)
    add_assistant_message("```json")
    
    response = send({
        "stop_sequences": ["```"],
    }, print_response=False)
    return json.loads(response)

def validate_json(text):
    try:
        json.loads(text.strip())
        return 10
    except json.JSONDecodeError:
        return 0

def validate_python(text):
    try:
        ast.parse(text.strip())
        return 10
    except SyntaxError:
        return 0

def validate_regex(text):
    try:
        re.compile(text.strip())
        return 10
    except re.error:
        return 0

def grade_syntax(test_case, output):
    if test_case["format"] == "json":
        return validate_json(output)
    elif test_case["format"] == "python":
        return validate_python(output)
    elif test_case["format"] == "regex":
        return validate_regex(output)
    else:
        raise ValueError(f"Unknown format: {test_case['format']}")

results = []

with open("dataset-scoring.json", "r") as f:
    dataset = json.load(f)
for test_case in dataset:
    prompt = f"""
Please solve the following task:

{test_case["task"]}
"""
    
    clear_messages()
    add_user_message(prompt)
    output = send(print_response=False)

    # Grade the output
    model_grade = grade_by_model(test_case, output)
    syntax_score = grade_syntax(test_case, output)
    
    result = {
        "output": output,
        "test_case": test_case,
        "score": (model_grade["score"] + syntax_score) / 2,
        "reasoning": model_grade["reasoning"]
    }
    results.append(result)

average_score = mean([result["score"] for result in results])
print(f"Average score: {average_score}")

if os.path.exists("score.json"):
    os.remove("score.json")
with open("score.json", "w") as f:
    json.dump(results, f, indent=2)
