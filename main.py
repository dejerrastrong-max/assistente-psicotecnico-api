
import os
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("assistente")

app = FastAPI(title="Assistente Psicotécnico Angola")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
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


@app.get("/saude")
def saude():
    return {
        "servidor": "online",
        "chave_configurada": bool(API_KEY),
    }


@app.post("/analisar")
def analisar(dados: Pergunta):
    if not client:
        raise HTTPException(
            status_code=500,
            detail="A chave GEMINI_API_KEY não está configurada no Render.",
        )

    if not dados.pergunta.strip():
        raise HTTPException(
            status_code=400,
            detail="Escreve uma pergunta.",
        )

    prompt = f"""
És um tutor de raciocínio psicotécnico.
Analisa a pergunta e as alternativas fornecidas.
Explica o raciocínio passo a passo e indica a resposta mais provável.
Explica porquê. Se faltarem dados ou houver ambiguidade,
avisa claramente. Não inventes certezas.

Pergunta: {dados.pergunta}
Alternativas: {dados.alternativas}
"""

    try:
        resposta = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt,
        )

        texto = getattr(resposta, "text", None)

        if not texto:
            raise RuntimeError("A Gemini devolveu uma resposta vazia.")

        return {"resposta": texto}

    except Exception as e:
        logger.exception("ERRO GEMINI")
        raise HTTPException(
            status_code=502,
            detail=f"Erro da IA: {type(e).__name__}: {e}",
        ) from e
