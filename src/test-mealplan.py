import json
import os
from statistics import mean
from utils.ai import add_user_message, add_assistant_message, clear_messages, send

if not os.path.exists("dataset-mealplan.json"):
    exit("Dataset file 'dataset-mealplan.json' not found. Please run 'create-mealplan-dataset.py' first.")

def grade_by_model(test_case, output):
    # Create evaluation prompt
    eval_prompt = f"""
You are an expert in nutrition and meal planning. Evaluate this AI-generated solution.

<task>
{test_case["task"]}
</task>
<solution>
{output}
</solution>
<athlete_information>
    <height>{test_case["height"]}</height>
    <weight>{test_case["weight"]}</weight>
    <goal>{test_case["goal"]}</goal>
    <restrictions>{test_case["restrictions"]}</restrictions>
</athlete_information>

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
        "model": "claude-haiku-4-5",
        "stop_sequences": ["```"],
    }, print_response=False)
    return json.loads(response)

results = []

with open("dataset-mealplan.json", "r") as f:
    dataset = json.load(f)
for test_case in dataset:
    prompt = f"""
Generate a one-day meal plan for an athlete that meets their dietary restrictions.
Make sure the output is short within limit of 1000 tokens.

<task>
{test_case["task"]}
</task>

<athlete_information>
<height>{test_case["height"]}</height>
<weight>{test_case["weight"]}</weight>
<goal>{test_case["goal"]}</goal>
<restrictions>{test_case["restrictions"]}</restrictions>
</athlete_information>

The output should include:
- Daily caloric total
- Macronutrient breakdown  
- Meals with exact foods, portions, and timing

<guidelines>
1. Include accurate daily calorie amount
2. Show protein, fat, and carb amounts  
3. Specify when to eat each meal
4. Use only foods that fit restrictions
5. List all portion sizes in grams
6. Keep budget-friendly if mentioned
</guidelines>
"""
    
    clear_messages()
    add_user_message(prompt)
    output = send(print_response=False)
    model_grade = grade_by_model(test_case, output)
    results.append({
        "test_case": test_case,
        "output": output,
        "model_grade": model_grade
    })

average_score = mean([result["model_grade"]["score"] for result in results])
print(f"Average score: {average_score}")
    
with open("results-mealplan.json", "w") as f:
    json.dump(results, f, indent=2)
