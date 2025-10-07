# main.py
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def home():
    return {"status": "online"}

@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()
    print("Mensagem recebida:", data)
    return {"resposta": "oi"}
