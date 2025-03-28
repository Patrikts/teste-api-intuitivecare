from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from rapidfuzz import process, fuzz

app = FastAPI()

# CORS (para permitir requisições do frontend em Vue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ajuste conforme necessário
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carrega o CSV na inicialização
df = pd.read_csv("relatorio_cadop.csv", sep=";", encoding="latin1")

# Converte para lowercase para facilitar a busca
df['RAZAO SOCIAL'] = df['RAZAO SOCIAL'].str.lower()

@app.get("/buscar")
def buscar_operadora(q: str = Query(..., description="Termo de busca")):
    termo = q.lower()
    razoes_sociais = df['RAZAO SOCIAL'].tolist()
    
    # Busca por similaridade (top 5 resultados)
    resultados = process.extract(termo, razoes_sociais, scorer=fuzz.WRatio, limit=5)

    matches = []
    for match, score, idx in resultados:
        row = df.iloc[idx]
        matches.append({
            "razao_social": row['RAZAO SOCIAL'],
            "registro_ans": row['REGISTRO ANS'],
            "cnpj": row['CNPJ'],
            "uf": row['UF'],
            "municipio": row['MUNICIPIO'],
            "pontuacao": score
        })

    return {"termo_busca": termo, "resultados": matches}
