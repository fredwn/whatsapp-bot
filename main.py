# main.py
import os
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "meu_token_secreto")

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/webhook", response_class=PlainTextResponse)
def verify(hub_mode: str = "", hub_challenge: str = "", hub_verify_token: str = ""):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge
    return "forbidden"

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Mensagem recebida:", data)
    return {"resposta": "oi"}
