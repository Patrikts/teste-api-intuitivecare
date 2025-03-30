from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from rapidfuzz import process, fuzz
import re

app = FastAPI()

# Habilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para limpar CNPJ
def limpar_cnpj(texto):
    return re.sub(r"[^\d]", "", texto or "")

# Carrega o CSV
df = pd.read_csv("relatorio_cadop.csv", sep=";", encoding="latin1")

# Padroniza as colunas usadas
for col in ["Razao_Social", "Nome_Fantasia", "CNPJ"]:
    df[col] = df[col].astype(str).fillna("").str.lower()

# Endpoint principal
@app.get("/buscar")
def buscar_operadora(
    q: str = Query(..., description="Termo de busca"),
    uf: str = Query(None, description="Filtrar por UF"),
    cidade: str = Query(None, description="Filtrar por cidade"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=50)
):
    termo = q.lower()
    df_filtrado = df.copy()

    if uf:
        df_filtrado = df_filtrado[df_filtrado["UF"].str.lower() == uf.lower()]
    if cidade:
        df_filtrado = df_filtrado[df_filtrado["Cidade"].str.lower() == cidade.lower()]

    # Concatena com fallback para campos vazios
    busca_em = (
        df_filtrado["Razao_Social"].fillna("") + " " +
        df_filtrado["Nome_Fantasia"].fillna("") + " " +
        df_filtrado["CNPJ"].fillna("")
    ).tolist()

    resultados = process.extract(termo, busca_em, scorer=fuzz.WRatio, limit=100)

    matches = []
    for _, score, idx in resultados:
        row = df_filtrado.iloc[idx]
        matches.append({
            "razao_social": row["Razao_Social"],
            "nome_fantasia": row["Nome_Fantasia"],
            "registro_ans": row["Registro_ANS"],
            "cnpj": row["CNPJ"],
            "uf": row["UF"],
            "municipio": row["Cidade"],
            "pontuacao": score
        })

    start = (page - 1) * limit
    end = start + limit
    paginated = matches[start:end]

    return {
        "termo_busca": termo,
        "total_encontrado": len(matches),
        "pagina": page,
        "por_pagina": limit,
        "resultados": paginated
    }