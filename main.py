from duckduckgo_search import DDGS
from huggingface_hub import InferenceClient
import json
import os
from dotenv import load_dotenv
from rag import query_documents, generate_response

load_dotenv()

client = InferenceClient(token=os.getenv("HF_TOKEN"))

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

# Agent loop
def run_agent(user_question: str):
    messages = [
        {
            "role": "system",
            "content": """You are a helpful agent with these tools:
            - search_documents(query): search internal documents
            - search_web(query): search the internet
            - calculator(expression): do math
            - get_current_date(): get today's date

            Always respond in valid JSON only:
            {"tool": "tool_name", "input": "your input"}
            
            When you have enough info to answer:
            {"tool": "none", "answer": "your final answer"}
            """
        },
        {"role": "user", "content": user_question}
    ]

    while True:
        response = client.chat_completion(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=messages,
            max_tokens=512
        )

        reply = response.choices[0].message.content
        
        try:
            parsed = json.loads(reply)
        except:
            return reply  # model gave direct answer

        # Final answer
        if parsed["tool"] == "none":
            return parsed["answer"]

        # Call the tool
        tool_name = parsed["tool"]
        tool_input = parsed.get("input", "")
        
        print(f"🔧 Using tool: {tool_name} with input: {tool_input}")
        
        if tool_name in available_tools:
            if tool_input:
                tool_result = available_tools[tool_name](tool_input)
            else:
                tool_result = available_tools[tool_name]()
        else:
            tool_result = "Tool not found"

        # Feed result back to agent
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": f"Tool result: {tool_result}"})

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
       quit
    """)

# Run it
while True:
    question = input("You: ")
    if question.lower() == "quit":
        break
    answer = run_agent(question)
    print(f"Agent: {answer}\n")