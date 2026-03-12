from groq import Groq
import os
from dotenv import load_dotenv
from main import get_answer

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Test cases with known answers
test_cases = [
    {"question": "Who won the 2013 Champions League Final?", "expected": "Bayern Munich"},
    {"question": "Who won Ballon d'Or in 2018?", "expected": "Luka Modric"},
    {"question": "Who won the 2022 World Cup?", "expected": "Argentina"},
    {"question": "Who scored in the 2016 Champions League Final?", "expected": "Ramos"},
    {"question": "Who won the 2014 World Cup?", "expected": "Germany"},
]

# LLM as judge
def evaluate_answer(question, expected, actual):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"""
                Question: {question}
                Expected answer contains: {expected}
                Actual answer: {actual}
                
                Does the actual answer correctly address the question 
                and contain the expected information?
                Reply with only: PASS or FAIL and one sentence why.
                """
            }
        ],
        max_tokens=100
    )
    return response.choices[0].message.content

# Run evals
def run_evals():
    passed = 0
    for test in test_cases:
        answer = get_answer(test["question"])
        verdict = evaluate_answer(test["question"], test["expected"], answer)
        status = "✅" if "PASS" in verdict else "❌"
        if "PASS" in verdict:
            passed += 1
        print(f"{status} {test['question']}")

    print(f"\nScore: {passed}/{len(test_cases)} ({(passed/len(test_cases))*100:.0f}%)")

run_evals()


"""

## Expected Output Now

✅ Who won the 2013 Champions League Final?
❌ Who won Ballon d'Or in 2018?
✅ Who won the 2022 World Cup?
❌ Who scored in the 2016 Champions League Final?
✅ Who won the 2014 World Cup?

Score: 3/5 (60%)

"""