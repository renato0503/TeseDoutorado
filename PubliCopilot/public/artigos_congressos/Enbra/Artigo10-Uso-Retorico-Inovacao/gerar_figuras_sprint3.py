import csv
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 150

# === FIGURA 1: Distribuição das Categorias (dados do artigo - Tabela 1) ===
categorias = ['Mero Mimetismo\nTecnológico', 'Inovação\nLegítima', 'Urgência e\nExcepcionalidade\nRetórica', 'Redundância\nInstrumental']
frequencias = [33.43, 31.43, 17.71, 17.43]
cores_cat = ['#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(categorias, frequencias, color=cores_cat, edgecolor='white', height=0.6)
for bar, val in zip(bars, frequencias):
    ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
            f'{val:.2f}%', va='center', fontsize=11, fontweight='bold')
ax.set_xlabel('Incidência Relativa (%)', fontsize=12)
ax.set_title('Distribuição das Categorias Discursivas no Corpus (N = 350)', fontsize=13, fontweight='bold')
ax.set_xlim(0, 42)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('figura1_categorias_retoricas.png', dpi=150, bbox_inches='tight')
plt.close()
print('figura1_categorias_retoricas.png criada')

# === FIGURA 2: RS Competitivo vs. Contratação Direta ===
modalidades = ['Certames\nCompetitivos', 'Contratações\nDiretas']
rs_means = [0.4308, 0.7574]
rs_std = [0.12, 0.15]
cores_rs = ['#3498db', '#e74c3c']

fig, ax = plt.subplots(figsize=(6, 5))
bars = ax.bar(modalidades, rs_means, yerr=rs_std, color=cores_rs, edgecolor='white',
              capsize=8, width=0.5, error_kw={'linewidth': 2})
ax.axhline(y=0.50, color='gray', linestyle='--', linewidth=1.5, label='Threshold Retórico (RS=0,50)')
for bar, val in zip(bars, rs_means):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
            f'{val:.4f}', ha='center', fontsize=12, fontweight='bold')
ax.set_ylabel('Rhetorical Score (RS) Médio', fontsize=12)
ax.set_title('Intensidade Retórica por Modalidade de Contratação', fontsize=13, fontweight='bold')
ax.set_ylim(0, 1.0)
ax.legend(fontsize=10)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('figura2_rs_por_modalidade.png', dpi=150, bbox_inches='tight')
plt.close()
print('figura2_rs_por_modalidade.png criada')

# === FIGURA 3: Word Cloud dos termos mais frequentes ===
termos_retoricos = {
    'inovação': 45, 'tecnologia': 38, 'digital': 32, 'solução': 28,
    'blockchain': 22, 'inteligência artificial': 20, 'deep learning': 18,
    'transformação digital': 17, 'disruptivo': 16, 'modernização': 15,
    'machine learning': 14, 'urgência': 13, 'big data': 12, 'governança': 11,
    'inexigibilidade': 11, 'sinergia': 10, 'otimização': 10, 'cloud computing': 9,
    'metaverso': 9, 'complexidade': 8, 'exponencial': 8, 'sustentabilidade': 7,
    'vanguarda': 7, 'compliance': 6, 'accountability': 5, 'paradigmático': 5,
    'único': 4, 'resiliência': 4, 'revolucionário': 4, 'smart': 3
}

wc = WordCloud(
    width=1200, height=600,
    background_color='white',
    colormap='viridis',
    max_words=30,
    random_state=42,
    prefer_horizontal=0.7
).generate_from_frequencies(termos_retoricos)

fig, ax = plt.subplots(figsize=(10, 5))
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
ax.set_title('Termos mais Frequentes em Justificativas Retóricas (RS > 0,5)', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('figura3_wordcloud_retorica.png', dpi=150, bbox_inches='tight')
plt.close()
print('figura3_wordcloud_retorica.png criada')

print('\nTodas as figuras foram criadas!')
