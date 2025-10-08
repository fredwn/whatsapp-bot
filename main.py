# main.py
import os, json
from fastapi import FastAPI, Request, Query
from fastapi.responses import PlainTextResponse, JSONResponse
import requests

app = FastAPI()

# Pegue estes valores em Variables no Railway (NÃO coloque credenciais no código):
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "meu_token_secreto")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID", "")   # ex.: 123456789012345
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "")         # token da Meta

@app.get("/")
def home():
    return {"status": "online"}

# Verificação do webhook (Meta envia hub.*)
@app.get("/webhook", response_class=PlainTextResponse)
def verify(
    hub_mode: str = Query(default="", alias="hub.mode"),
    hub_challenge: str = Query(default="", alias="hub.challenge"),
    hub_verify_token: str = Query(default="", alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge
    return "forbidden"

# Recebimento de mensagens → responde "oi" no WhatsApp
@app.post("/webhook")
async def webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid json"}, status_code=400)

    # DEBUG: confira se o app está lendo as variáveis corretas
    print("DEBUG PHONE_NUMBER_ID:", PHONE_NUMBER_ID)
    if ACCESS_TOKEN:
        print("DEBUG ACCESS_TOKEN:", ACCESS_TOKEN[:8], "...", ACCESS_TOKEN[-8:])
    else:
        print("DEBUG ACCESS_TOKEN: (vazio)")

    try:
        entry = data["entry"][0]
        change = entry["changes"][0]
        value = change["value"]
        messages = value.get("messages", [])
        if not messages:
            return {"status": "ignored"}

        from_number = messages[0]["from"]

        url = f"https://graph.facebook.com/v20.0/{PHONE_NUMBER_ID}/messages"
        payload = {
            "messaging_product": "whatsapp",
            "to": from_number,
            "type": "text",
            "text": {"body": "oi"},
        }
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json",
        }
        print("DEBUG POST URL:", url)
        r = requests.post(url, headers=headers, json=payload)
        print("Resposta enviada:", r.status_code, r.text)
    except Exception as e:
        print("Erro ao processar/enviar:", repr(e))

    return {"status": "ok"}
