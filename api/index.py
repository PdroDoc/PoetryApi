from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import requests
import random

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "API de poesia funcionando. Be Aware."}

@app.get("/poesia")
def poesia(keyword: str = Query(None, description="Palavra-chave para busca no poema")):
    if keyword:
        url = f"https://poetrydb.org/lines/{keyword}"
    else:
        url = "https://poetrydb.org/random"

    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()

        if isinstance(dados, dict) and dados.get("status") == 404:
            return JSONResponse(content={"erro": "Nenhum poema encontrado para essa palavra."}, status_code=404)

        poema = random.choice(dados) if keyword else dados[0]

        return {
            "titulo": poema.get("title"),
            "autor": poema.get("author"),
            "versos": poema.get("lines")
        }

    return JSONResponse(content={"erro": "Erro ao buscar na PoetryDB."}, status_code=500)