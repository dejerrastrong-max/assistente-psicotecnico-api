
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Assistente Psicotécnico Angola")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None

class Pergunta(BaseModel):
    pergunta: str
    alternativas: str = ""

@app.get("/")
def inicio():
    return {"estado": "Assistente psicotécnico online"}

@app.post("/analisar")
def analisar(dados: Pergunta):
    if not client:
        raise HTTPException(500, "A chave de IA ainda não foi configurada.")
    if not dados.pergunta.strip():
        raise HTTPException(400, "Escreve uma pergunta.")

    prompt = f"""
És um tutor de raciocínio psicotécnico.
Analisa a pergunta e as alternativas fornecidas.
Explica o raciocínio passo a passo, indica a resposta mais provável
e explica porquê. Se faltarem dados ou houver ambiguidade,
avisa claramente. Não inventes certezas.

Pergunta: {dados.pergunta}
Alternativas: {dados.alternativas}
"""
    try:
        resposta = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return {"resposta": resposta.text}
        except Exception as e:
        print("ERRO GEMINI:", repr(e), flush=True)
        raise HTTPException(
            status_code=502,
            detail=f"Erro da IA: {type(e).__name__}: {e}"
        )
