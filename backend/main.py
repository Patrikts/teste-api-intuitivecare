from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from rapidfuzz import process, fuzz
import re

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Função para limpar pontuação do CNPJ
def limpar_cnpj(texto):
    return re.sub(r"[^\d]", "", texto or "")

# Carregar CSV
df = pd.read_csv("relatorio_cadop.csv", sep=";", encoding="latin1")

# Padroniza colunas para texto minúsculo e sem erros
for col in ['Razao_Social', 'Nome_Fantasia', 'CNPJ']:
    df[col] = df[col].astype(str).str.lower()

# Endpoint principal com filtros e paginação
@app.get("/buscar")
def buscar_operadora(
    q: str = Query(..., description="Termo de busca (nome, fantasia ou CNPJ)"),
    uf: str = Query(None, description="Filtrar por UF"),
    cidade: str = Query(None, description="Filtrar por cidade"),
    page: int = Query(1, ge=1, description="Página"),
    limit: int = Query(10, ge=1, le=50, description="Limite por página")
):
    termo = q.lower()

    df_filtrado = df.copy()
    if uf:
        df_filtrado = df_filtrado[df_filtrado["UF"].str.lower() == uf.lower()]
    if cidade:
        df_filtrado = df_filtrado[df_filtrado["Cidade"].str.lower() == cidade.lower()]

    busca_em = (
        df_filtrado['Razao_Social'] + " " +
        df_filtrado['Nome_Fantasia'] + " " +
        df_filtrado['CNPJ']
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

# Endpoint detalhado buscando especificamente CNPJ, Razão Social e Nome Fantasia
@app.get("/buscar-detalhado")
def buscar_detalhado(
    termo: str = Query(..., description="Busca por CNPJ, Razao_Social ou Nome_Fantasia"),
    limit: int = Query(10, ge=1, le=50)
):
    termo_limpo = termo.lower()
    termo_sem_pontuacao = limpar_cnpj(termo_limpo)

    def gerar_chave(row):
        return " ".join([
            limpar_cnpj(row["CNPJ"]),
            str(row["Razao_Social"]).lower(),
            str(row["Nome_Fantasia"]).lower()
        ])

    combinados = df.apply(gerar_chave, axis=1).tolist()

    resultados = process.extract(termo_sem_pontuacao or termo_limpo, combinados, scorer=fuzz.WRatio, limit=limit)

    retorno = []
    for _, score, idx in resultados:
        row = df.iloc[idx]
        retorno.append({
            "cnpj": row["CNPJ"],
            "razao_social": row["Razao_Social"],
            "nome_fantasia": row["Nome_Fantasia"],
            "registro_ans": row["Registro_ANS"],
            "uf": row["UF"],
            "municipio": row["Cidade"],
            "pontuacao": score
        })

    return {
        "termo_busca": termo,
        "resultados": retorno
    }