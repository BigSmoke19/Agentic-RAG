# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"error": "Too many requests."})

# ✅ Import RAG lazily — only when first request comes in
rag_loaded = False
query_documents = None
generate_response = None

def load_rag():
    global rag_loaded, query_documents, generate_response
    if not rag_loaded:
        print("Loading RAG pipeline...")
        from rag import query_documents as qd, generate_response as gr
        query_documents = qd
        generate_response = gr
        rag_loaded = True
        print("RAG pipeline loaded ✅")

# ✅ Import agent lazily too
agent_loaded = False
run_agent_func = None

def load_agent():
    global agent_loaded, run_agent_func
    if not agent_loaded:
        print("Loading agent...")
        from agent import run_agent
        run_agent_func = run_agent
        agent_loaded = True
        print("Agent loaded ✅")

class QuestionRequest(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "Football RAG Agent is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
@limiter.limit("5/minute")
def ask(request: Request, body: QuestionRequest):
    load_agent()  # loads only on first request
    result = run_agent_func(body.question, silent=True)
    return {
        "answer": result["answer"],
        "tools_used": result["tools_used"]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)