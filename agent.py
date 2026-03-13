from ddgs import DDGS
from groq import Groq
import json
import os
from dotenv import load_dotenv
from rag import query_documents, generate_response
import re

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define your tools
def search_web(query: str) -> str:
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(query, max_results=3)]
        return "\n".join([r["body"] for r in results])

def calculator(expression: str) -> str:
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

def get_current_date() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d")

def search_documents(query: str) -> str:
    chunks = query_documents(query)
    response = generate_response(query, chunks)
    return "\n".join(response)

available_tools = {
    "search_documents": search_documents,
    "search_web": search_web,
    "calculator": calculator,
    "get_current_date": get_current_date
}

import re

def extract_json(text: str) -> dict:
    """Extract JSON from model response even if it has extra text around it"""
    # Try direct parse first
    try:
        return json.loads(text)
    except:
        pass
    
    # Try to find JSON pattern in the text
    try:
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except:
        pass
    
    # No JSON found — treat as final answer
    return {"tool": "none", "answer": text}


def run_agent(user_question: str, silent: bool = False):
    messages = [
        {
            "role": "system",
            "content": """You are a helpful agent with these tools:
            - search_documents(query): search internal football documents ONLY
            - search_web(query): search the internet for any general knowledge
            - calculator(expression): do math
            - get_current_date(): get today's date

            RULES:
            1. For football questions → use search_documents FIRST
            2. For non-football questions → use search_web DIRECTLY
            3. If search_documents returns garbage → switch to search_web immediately
            4. NEVER search for the same thing twice
            5. After getting a tool result → give final answer immediately
            6. If results are imperfect → still give best answer from available info

            Always respond in valid JSON only — no extra text, no explanation:
            {"tool": "tool_name", "input": "your input"}
            
            When you have enough info to answer:
            {"tool": "none", "answer": "your final answer"}
            """
        },
        {"role": "user", "content": user_question}
    ]

    tools_used = []

    for iteration in range(5):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=512
        )

        reply = response.choices[0].message.content

        parsed = extract_json(reply)

        if parsed["tool"] == "none":
            return {"answer": parsed["answer"], "tools_used": tools_used}

        tool_name = parsed["tool"]
        tool_input = parsed.get("input", "")

        # Prevent duplicate tool calls
        already_used = any(
            t["tool"] == tool_name and t["input"] == tool_input
            for t in tools_used
        )
        if already_used:
            return {
                "answer": "Could not find a definitive answer.",
                "tools_used": tools_used
            }

        tools_used.append({"tool": tool_name, "input": tool_input})

        if not silent:
            print(f"🔧 Using tool: {tool_name} with input: {tool_input}")

        if tool_name in available_tools:
            tool_result = available_tools[tool_name](tool_input) if tool_input else available_tools[tool_name]()
        else:
            tool_result = "Tool not found"

        messages.append({"role": "assistant", "content": reply})
        messages.append({
            "role": "user",
            "content": f"Tool result: {tool_result}\n\nNow give your final answer immediately."
        })

    return {"answer": "Could not complete within allowed steps.", "tools_used": tools_used}

def get_result(user_question: str) -> str:
    """Clean function that returns result - use this for api"""
    result = run_agent(user_question)
    return result

def get_answer(user_question: str) -> str:
    """Clean function that returns just the answer string - use this for evals"""
    result = run_agent(user_question)
    return result["answer"]

if __name__ == "__main__":

    print("""
        > Available Options:    
        - search documents(query): search internal Football documents
        - search web(query): search the internet
        - calculator(expression): do math
        - get current date: get today's date\n
        e.g queries
        who won the champions league final in 2013?
        3*8+2
        display current date
        quit\n
        """)

    # Run it# Run it
    while True:
        question = input("You: ")
        if question.lower() == "quit":
            print("Goodbye!")
            break
        
        result = run_agent(question)
        
        print(f"\nAgent: {result['answer']}")
        
        if result['tools_used']:
            print(f"🔧 Tools used: {[t['tool'] for t in result['tools_used']]}")
        
        print()