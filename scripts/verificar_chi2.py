import numpy as np
from scipy import stats

# Dados da Tabela 2 - Matriz de Contingência Observada
observado = np.array([
    [54, 36, 2, 0],    # Lei nº 8.666/1993
    [28, 18, 12, 2],   # Lei nº 12.462/2011 (RDC)
    [35, 15, 28, 8],   # Lei nº 13.303/2016 (Estatais)
    [78, 42, 65, 18],  # Lei nº 14.133/2021 (NLLC)
    [4, 3, 26, 45]     # LC nº 182/2021 (Startups)
])

# Totais de linha e coluna
totais_linha = observado.sum(axis=1)
totais_coluna = observado.sum(axis=0)
grand_total = observado.sum()

print("=" * 60)
print("VERIFICAÇÃO DO TESTE QUI-QUADRADO")
print("=" * 60)
print()
print("Matriz Observada (Tabela 2 do artigo):")
print(f"{'':20s} {'C1':>8} {'C2':>8} {'C3':>8} {'C4':>8} {'Total':>8}")
for i, (lei, row) in enumerate(zip(['8.666/1993', '12.462 (RDC)', '13.303 (Estatais)', '14.133 (NLLC)', 'LC 182 (Startups)'], observado)):
    print(f"{lei:20s} {row[0]:>8} {row[1]:>8} {row[2]:>8} {row[3]:>8} {totais_linha[i]:>8}")
print(f"{'Total':20s} {totais_coluna[0]:>8} {totais_coluna[1]:>8} {totais_coluna[2]:>8} {totais_coluna[3]:>8} {grand_total:>8}")
print()

# Calcular matriz esperada sob H0 (independência)
esperado = np.outer(totais_linha, totais_coluna) / grand_total

print("Matriz Esperada sob H0 (independência):")
print(f"{'':20s} {'C1':>8} {'C2':>8} {'C3':>8} {'C4':>8}")
for i, lei in enumerate(['8.666/1993', '12.462 (RDC)', '13.303 (Estatais)', '14.133 (NLLC)', 'LC 182 (Startups)']):
    print(f"{lei:20s} {esperado[i,0]:>8.2f} {esperado[i,1]:>8.2f} {esperado[i,2]:>8.2f} {esperado[i,3]:>8.2f}")
print()

# Calcular Qui-Quadrado manualmente
chi2 = ((observado - esperado) ** 2 / esperado).sum()
graus_liberdade = (observado.shape[0] - 1) * (observado.shape[1] - 1)
p_valor = 1 - stats.chi2.cdf(chi2, graus_liberdade)

print("=" * 60)
print("RESULTADO DO TESTE")
print("=" * 60)
print(f"Estatística χ² calculada: {chi2:.4f}")
print(f"Artigo reporta:           216,1380")
print(f"Diferença:                {abs(chi2 - 216.1380):.4f}")
print()
print(f"Graus de liberdade:       {graus_liberdade}")
print(f"p-valor:                 {p_valor:.2e} (< 0,001)")
print()

if abs(chi2 - 216.1380) < 0.01:
    print("✅ VERIFICAÇÃO: χ² calculado CONFIRMA o valor reportado no artigo!")
else:
    print("⚠️ ATENÇÃO: Diferença encontrada - verificar metodologia do artigo")
print()

# Medidas de efeito
n = grand_total
k = 5  # número de categorias de legislação
m = 4  # número de categorias semânticas
phi2 = chi2 / n
c = np.sqrt(phi2 / (np.sqrt((k-1)*(m-1))))
v = np.sqrt(phi2 / min(k-1, m-1))

print("=" * 60)
print("MEDIDAS DE EFEITO")
print("=" * 60)
print(f"Coeficiente de Contingência C: {c:.4f}")
print(f"V de Cramér:                 {v:.4f}")
print(f"Phi² / n:                    {phi2:.4f}")
print()

# Contribuição de cada célula para o χ² total
contribuicoes = ((observado - esperado) ** 2 / esperado)
print("=" * 60)
print("PRINCIPAIS CONTRIBUINTES PARA χ²")
print("=" * 60)
contribuicoes_flat = []
for i, lei in enumerate(['8.666/1993', '12.462', '13.303', '14.133', 'LC 182']):
    for j, cat in enumerate(['C1', 'C2', 'C3', 'C4']):
        contribuicoes_flat.append((lei, cat, contribuicoes[i,j]))

contribuicoes_flat.sort(key=lambda x: x[2], reverse=True)
for lei, cat, cont in contribuicoes_flat[:10]:
    print(f"  {lei} + {cat}: {cont:.2f} ({cont/chi2*100:.1f}%)")

print()
print("=" * 60)
print("ÍNDICES SINTÉTICOS")
print("=" * 60)

# Calcular IGR e IIN para cada legislação
leis = ['8.666/1993', '12.462 (RDC)', '13.303 (Estatais)', '14.133 (NLLC)', 'LC 182 (Startups)']
for i, lei in enumerate(leis):
    C1, C2, C3, C4 = observado[i]
    total = totais_linha[i]
    IGR = (C3 + C4) / (C1 + C2) if (C1 + C2) > 0 else 0
    IIN = C4 / (C1 + C2 + C3 + C4) if total > 0 else 0
    print(f"{lei}:")
    print(f"  IGR (Governança) = ({C3}+{C4})/({C1}+{C2}) = {IGR:.4f}")
    print(f"  IIN (Inovabilidade) = {C4}/{total} = {IIN:.4f}")
    print()