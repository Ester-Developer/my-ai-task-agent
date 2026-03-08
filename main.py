from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent_service import run_agent
import todo_service

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    message: str

@app.get("/tasks")
def list_tasks():
    return todo_service.get_tasks()

@app.post("/chat")
async def chat(request: ChatRequest):
    reply = run_agent(request.message)
    return {"reply": reply}