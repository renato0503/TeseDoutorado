import pandas as pd
import os

caminho_csv = os.path.join(os.path.dirname(__file__), "dados", "dataset_pncp.csv")

buzzwords_retoricas = [
    "urgente", "emergencial", "imprescindível", "inadiável",
    "inteligência artificial", "blockchain", "disruptivo", "ecossistema", 
    "inovador", "estado da arte", "revolucionário", "deep learning", "machine learning"
]

def calcular_rhetorical_score(text):
    if not isinstance(text, str):
        return 0.0
    text = text.lower()
    total_words = len(text.split())
    if total_words == 0:
        return 0.0
        
    buzz_count = sum(text.count(b) for b in buzzwords_retoricas)
    # Score normalizado (exemplo: max 1.0)
    score = (buzz_count / max(1, (total_words / 100))) # Buzzwords per 100 words
    return min(1.0, score)

print("Iniciando Análise de Conteúdo (Mineração de Texto) - Artigo 10...")
df = pd.read_csv(caminho_csv, sep=";")

df['texto_completo'] = df['justificativaPresencial'].fillna('') + " " + df['objetoCompra'].fillna('')

df['rhetorical_score'] = df['texto_completo'].apply(calcular_rhetorical_score)

df_valid = df[df['texto_completo'].str.strip() != '']
media_rs = df_valid['rhetorical_score'].mean()
alta_retorica = len(df_valid[df_valid['rhetorical_score'] > 0.5])
perc_alta_retorica = (alta_retorica / len(df_valid)) * 100

print(f"Total de justificativas analisadas: {len(df_valid)}")
print(f"Rhetorical Score Médio: {media_rs:.4f}")
print(f"Processos com Alta Densidade Retórica (>0.5): {alta_retorica} ({perc_alta_retorica:.2f}%)")

caminho_saida = os.path.join(os.path.dirname(__file__), "dados", "dataset_analisado.csv")
df_valid.to_csv(caminho_saida, index=False, sep=";")
print(f"Dataset analisado salvo em: {caminho_saida}")
