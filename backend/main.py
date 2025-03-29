from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from rapidfuzz import process, fuzz

app = FastAPI()

# CORS (permitir acesso do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega o CSV na inicialização
df = pd.read_csv("relatorio_cadop.csv", sep=";", encoding="latin1")

# Padroniza nomes
df['Razao_Social'] = df['Razao_Social'].str.lower()

@app.get("/buscar")
def buscar_operadora(q: str = Query(..., description="Termo de busca")):
    termo = q.lower()
    razoes_sociais = df['Razao_Social'].tolist()

    # Busca fuzzy nos nomes
    resultados = process.extract(termo, razoes_sociais, scorer=fuzz.WRatio, limit=5)

    matches = []
    for match, score, idx in resultados:
        row = df.iloc[idx]
        matches.append({
            "razao_social": row['Razao_Social'],
            "registro_ans": row['Registro_ANS'],
            "cnpj": row['CNPJ'],
            "uf": row['UF'],
            "municipio": row['Cidade'],
            "pontuacao": score
        })

    return {"termo_busca": termo, "resultados": matches}
