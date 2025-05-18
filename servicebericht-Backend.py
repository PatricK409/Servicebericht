import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

# Umgebungsvariablen aus .env laden
load_dotenv()

# OpenAI API-Key aus Umgebungsvariable
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS-Middleware, erlaubt Zugriffe von deinem Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # im Prod. besser auf deine Domain einschränken
    allow_methods=["*"],
    allow_headers=["*"],
)

# Statische Dateien (Frontend) ausliefern
app.mount(
    path="/",
    app=StaticFiles(directory="static", html=True),
    name="static",
)

class VorschauText(BaseModel):
    text: str

@app.post("/api/ki-formulierung")
async def ki_formulieren(payload: VorschauText):
    """
    Nimmt den Vorschau-Text entgegen und gibt eine professionell formulierte Version zurück.
    """
    prompt = (
        "Formuliere folgenden technischen Bericht professionell in ganzen Sätzen auf Deutsch:\n\n"
        + payload.text
    )
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Du bist ein technischer Redakteur."},
                {"role": "user", "content": prompt},
            ],
        )
        return {"text": resp.choices[0].message.content}
    except Exception as e:
        return {"error": str(e)}

# Optional: Health-Check
@app.get("/api/health")
async def health():
    return {"status": "ok"}
