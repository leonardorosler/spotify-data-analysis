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
    
# top 10 artistas com mais seguidores 
def top10_artistas_seguidores(musicas: list) -> None:
    print("\n" + "="*60)
    print("  OPÇÃO 1 — TOP 10 ARTISTAS COM MAIS SEGUIDORES")
    print("="*60)

    artistas_seguidores = {} # dicionario: {artists_name: artist_followers}

    for musica in musicas:
        nome = musica.get('artist_name', '').strip()
        seguidores_str = musica.get('artist_followers', '0').strip()
        
        if not nome or not seguidores_str: # pula linhas com dados faltando
            continue

        try:
            seguidores = int(float(seguidores_str))
        except ValueError:
            continue # linha com dado corrompido == é ignorada
        # evita que versoes com menos seguidores sobrescrevam 
        if nome not in artistas_seguidores or seguidores > artistas_seguidores[nome]:
            artistas_seguidores[nome] = seguidores

    top10 = sorted(artistas_seguidores.items(), key=lambda par: par[1], reverse=True)[:10]

    print(f"\n  {'Pos':<5} {'Artista':<35} {'Seguidores':>15}")
    print("  " + "-"*57)

    for posicao, (artista, seguidores) in enumerate(top10, start=1):
        print(f"  {posicao:<5} {artista:<35} {seguidores:>15,}")

    print()
