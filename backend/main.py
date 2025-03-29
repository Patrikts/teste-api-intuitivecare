from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from rapidfuzz import process, fuzz

app = FastAPI()

# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega e prepara os dados
df = pd.read_csv("relatorio_cadop.csv", sep=";", encoding="latin1")

# Padroniza colunas usadas na busca
for col in ['Razao_Social', 'Nome_Fantasia', 'CNPJ']:
    df[col] = df[col].astype(str).str.lower()

@app.get("/buscar")
def buscar_operadora(
    q: str = Query(..., description="Termo de busca (nome, fantasia ou CNPJ)"),
    uf: str = Query(None, description="Filtrar por UF"),
    cidade: str = Query(None, description="Filtrar por cidade"),
    page: int = Query(1, ge=1, description="Página"),
    limit: int = Query(10, ge=1, le=50, description="Limite por página")
):
    termo = q.lower()

    # Filtra se UF e Cidade forem fornecidos
    df_filtrado = df.copy()
    if uf:
        df_filtrado = df_filtrado[df_filtrado["UF"].str.lower() == uf.lower()]
    if cidade:
        df_filtrado = df_filtrado[df_filtrado["Cidade"].str.lower() == cidade.lower()]

    # Combina campos de busca
    busca_em = (
        df_filtrado['Razao_Social'] + " " +
        df_filtrado['Nome_Fantasia'] + " " +
        df_filtrado['CNPJ']
    ).tolist()

    # Busca fuzzy
    resultados = process.extract(termo, busca_em, scorer=fuzz.WRatio, limit=100)

    # Constrói lista de resultados
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

    # Paginação
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
