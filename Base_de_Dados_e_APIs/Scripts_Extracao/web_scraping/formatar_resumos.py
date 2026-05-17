#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para formatar resumos e abstracts de todos os arquivos HTML dos artigos e tese.
Regra: Sem parágrafo (text-indent: 0) e espaçamento simples (line-height: 1).
"""

import os
import re

def main():
    dirs = [
        r"c:\Users\Renato\Documents\Doutorado\Artigos",
        r"c:\Users\Renato\Documents\Doutorado\Tese"
    ]
    
    html_files = []
    for d in dirs:
        if not os.path.exists(d):
            continue
        for root, _, files in os.walk(d):
            for file in files:
                if file.endswith(".html"):
                    html_files.append(os.path.join(root, file))
                    
    print(f"🔍 Encontrados {len(html_files)} arquivos HTML para análise.")
    
    for path in html_files:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Encontra o bloco <style>
        style_match = re.search(r"<style>(.*?)</style>", content, re.DOTALL | re.IGNORECASE)
        if style_match:
            style_content = style_match.group(1)
            
            # Filtra linhas antigas que continham .resumo
            lines = style_content.split("\n")
            new_lines = []
            for line in lines:
                if ".resumo" in line:
                    continue
                new_lines.append(line)
                
            # Regras limpas e estritas ABNT para Resumo e Abstract
            # text-indent: 0 (sem parágrafo), line-height: 1 (espaçamento simples)
            new_rules = """
        .resumo { text-indent: 0 !important; margin-bottom: 0.8cm; line-height: 1.15 !important; }
        .resumo p { text-indent: 0 !important; margin: 0 0 0.3cm 0 !important; line-height: 1.15 !important; }
            """
            
            new_style_content = "\n".join(new_lines) + new_rules
            new_content = content.replace(style_match.group(1), new_style_content)
            
            # Escreve o arquivo atualizado
            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"🟢 [Formatado] {os.path.basename(path)}")
        else:
            # Caso não tenha <style>, cria uma regra simples no head
            new_style = """<head>
    <style>
        .resumo { text-indent: 0 !important; margin-bottom: 0.8cm; line-height: 1.15 !important; }
        .resumo p { text-indent: 0 !important; margin: 0 0 0.3cm 0 !important; line-height: 1.15 !important; }
    </style>"""
            if "<head>" in content:
                new_content = content.replace("<head>", new_style)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(new_content)
                print(f"🟡 [Injetado Style] {os.path.basename(path)}")

if __name__ == "__main__":
    main()
