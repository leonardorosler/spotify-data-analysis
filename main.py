import csv
import os
import plotly.graph_objects as go
import plotly.express as px

NOME_ARQUIVO = "spotify_data clean.csv"

# leitura do csv
def ler_dados(nome_arquivo: str) -> list:    # lista
    if not os.path.exists(nome_arquivo):
        print(f"\n  [ERRO] Arquivo '{nome_arquivo}' não encontrado.")
        print("  Certifique‑se de que o arquivo está na mesma pasta que este script.\n")
        return []

    musicas = []

    with open(nome_arquivo, encoding='utf-8-sig') as arquivo:
        leitor = csv.DictReader(arquivo)
        for linha in leitor:
            musicas.append(linha)

    print(f"\n  [OK] {len(musicas)} músicas carregadas com sucesso!\n")
    return musicas

# função auxiliar parsing de gêneros
def extrair_generos(campo_genero: str) -> set:   # set - conjunto
    if not campo_genero or campo_genero.strip() in ('', '[]'):
        return set() # se nulo/vazio retorna conjunto vazio

    limpo = campo_genero.replace('[', '').replace(']', '')
    limpo = limpo.replace("'", '').replace('"', '') # remove aspas/apóstrofos

    # cria uma lista de genero sem espaços
    lista_generos = [g.strip().lower() for g in limpo.split(',') if g.strip()]
    return set(lista_generos)

# função auxiliar extração do ano de lançamento
def extrair_ano(campo_data: str) -> int:
    try:
        return int(str(campo_data).strip()[:4]) # pega os 4 primeiros caracteres
    except (ValueError, TypeError):
        return 0 # ano inválido == 'sem data'
    
