from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import os
import re
from rapidfuzz import process, fuzz

csv_path = "relatorio_cadop.csv"

def limpar_cnpj(texto):
    return re.sub(r"[^\d]", "", texto or "")

def corrigir_encoding(df):
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].apply(lambda x: x.encode("latin1").decode("utf-8") if isinstance(x, str) else x)
    return df

if os.path.exists(csv_path):
    try:
        df = pd.read_csv(csv_path, sep=";", encoding="latin1")
        df = corrigir_encoding(df)
        for col in ["Razao_Social", "Nome_Fantasia", "CNPJ"]:
            if col in df.columns:
                df[col] = df[col].astype(str).fillna("").str.lower()
            else:
                df[col] = ""
    except Exception as e:
        print("❌ Erro ao carregar CSV:", e)
        df = pd.DataFrame()
else:
    df = pd.DataFrame()

@api_view(["GET"])
def buscar_operadora(request):
    try:
        q = request.GET.get("q", "")
        uf = request.GET.get("uf", "")
        cidade = request.GET.get("cidade", "")
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 10))

        if df.empty:
            return Response({"erro": "CSV não carregado."}, status=500)

        df_filtrado = df.copy()
        if uf:
            df_filtrado = df_filtrado[df_filtrado.get("UF", "").str.lower() == uf.lower()]
        if cidade:
            df_filtrado = df_filtrado[df_filtrado.get("Cidade", "").str.lower() == cidade.lower()]

        busca_em = (
            df_filtrado.get("Razao_Social", "").fillna("") + " " +
            df_filtrado.get("Nome_Fantasia", "").fillna("") + " " +
            df_filtrado.get("CNPJ", "").fillna("")
        ).tolist()

        resultados = process.extract(q.lower(), busca_em, scorer=fuzz.WRatio, limit=100)

        matches = []
        for _, score, idx in resultados:
            row = df_filtrado.iloc[idx]
            matches.append({
                "razao_social": row.get("Razao_Social", ""),
                "nome_fantasia": row.get("Nome_Fantasia", ""),
                "registro_ans": row.get("Registro_ANS", ""),
                "cnpj": row.get("CNPJ", ""),
                "uf": row.get("UF", ""),
                "municipio": row.get("Cidade", ""),
                "pontuacao": score
            })

        start = (page - 1) * limit
        end = start + limit

        return Response({
            "termo_busca": q,
            "total_encontrado": len(matches),
            "pagina": page,
            "por_pagina": limit,
            "resultados": matches[start:end]
        })

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({"erro": str(e)}, status=500)
