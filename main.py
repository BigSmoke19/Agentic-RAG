from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from agent import get_result
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI()

# API Calls Limiter 
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Allow React frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Handle rate limit errors nicely
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests. Please wait a moment."}
    )

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
@limiter.limit("5/minute")  # max 5 requests per minute per IP
def ask(request: Request, body: QuestionRequest):
    result = get_result(body.question)
    return {
        "answer": result["answer"],
        "tools_used": result["tools_used"]
    }

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)