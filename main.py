# main.py
import os
from fastapi import FastAPI, Request, Query
from fastapi.responses import PlainTextResponse, JSONResponse

app = FastAPI()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "meu_token_secreto")

@app.get("/")
def home():
    return {"status": "online"}

# WhatsApp Webhook Verification (GET)
@app.get("/webhook", response_class=PlainTextResponse)
def verify(
    hub_mode: str = Query(default="", alias="hub.mode"),
    hub_challenge: str = Query(default="", alias="hub.challenge"),
    hub_verify_token: str = Query(default="", alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge
    return "forbidden"

# Recebimento de mensagens (POST)
@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid json"}, status_code=400)
    print("Mensagem recebida:", data)
    return {"resposta": "oi"}

