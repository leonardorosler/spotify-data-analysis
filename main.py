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
    lista_generos = []
    for g in limpo.split(','):
        if g.strip():
            lista_generos.append(g.strip().lower())
    return set(lista_generos)

# função auxiliar extração do ano de lançamento
def extrair_ano(campo_data: str) -> int:
    try:
        return int(str(campo_data).strip()[:4]) # pega os 4 primeiros caracteres
    except (ValueError, TypeError):
        return 0 # ano inválido == 'sem data'
    
# opção 1: top 10 artistas com mais seguidores (dicionário e lista)
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

# opção 2: top 15 musicas mais longas (lista)
def top15_musicas_mais_longas(musicas: list) -> None:
    print("\n" + "="*60)
    print("  OPÇÃO 2 — TOP 15 MÚSICAS MAIS LONGAS")
    print("="*60)

    lista_duracoes = []
    for m in musicas:
        if m.get('track_duration_min', '').strip() and _eh_numero(m['track_duration_min']):
            tupla = (
                float(m['track_duration_min']),
                m.get('track_name', 'Desconhecida').strip(),
                m.get('artist_name', 'Desconhecido').strip()
            )
            lista_duracoes.append(tupla)

    lista_duracoes.sort(key=lambda tupla: tupla[0], reverse=True)
    top15 = lista_duracoes[:15]

    print(f"\n  {'Pos':<5} {'Música':<40} {'Artista':<25} {'Duração':>10}")
    print("  " + "-"*82)

    for posicao, (duracao, musica, artista) in enumerate(top15, start=1):
        musica_trunc  = musica[:38]  + '..' if len(musica)  > 38 else musica
        artista_trunc = artista[:23] + '..' if len(artista) > 23 else artista
        print(f"  {posicao:<5} {musica_trunc:<40} {artista_trunc:<25} {duracao:>8.2f} min")

    print()

def _eh_numero(valor: str) -> bool:
    """Função auxiliar: retorna True se a string pode ser convertida em float."""
    try:
        float(valor)
        return True
    except (ValueError, TypeError):
        return False


# opção 3: comparação: músicas explícitas x não explícitas
def comparar_popularidade_explicitas(musicas: list) -> None:
    print("\n" + "="*60)
    print("  OPÇÃO 3 — POPULARIDADE MÉDIA: EXPLÍCITAS vs NÃO EXPLÍCITAS")
    print("="*60)

    grupos = {
        True:  [],
        False: []
    }

    for musica in musicas:
        explicita_str  = musica.get('explicit', '').strip().upper()
        popularidade_s = musica.get('track_popularity', '').strip()

        if not explicita_str or not popularidade_s:
            continue
        if not _eh_numero(popularidade_s):
            continue

        eh_explicita = (explicita_str == 'TRUE')
        popularidade = float(popularidade_s)
        grupos[eh_explicita].append(popularidade)

    media_explicita     = sum(grupos[True])  / len(grupos[True])  if grupos[True]  else 0
    media_nao_explicita = sum(grupos[False]) / len(grupos[False]) if grupos[False] else 0

    diferenca = abs(media_explicita - media_nao_explicita)
    vencedor  = "Explícitas" if media_explicita > media_nao_explicita else "Não‑Explícitas"

    print(f"\n  {'Categoria':<25} {'Qtd. Músicas':>15} {'Popularidade Média':>20}")
    print("  " + "-"*62)
    print(f"  {'🔴 Explícitas (TRUE)':<25} {len(grupos[True]):>15,} {media_explicita:>19.2f}")
    print(f"  {'🟢 Não‑Explícitas (FALSE)':<25} {len(grupos[False]):>15,} {media_nao_explicita:>19.2f}")
    print("  " + "-"*62)
    print(f"\n  📊 Diferença entre as médias : {diferenca:.2f} pontos")
    print(f"  🏆 Categoria mais popular    : {vencedor}")
    print()

# opção 4: cruzamento de genero com conjuntos
def cruzamento_generos_sets(musicas: list) -> None:
    print("\n" + "="*60)
    print("  OPÇÃO 4 — CRUZAMENTO DE GÊNEROS MUSICAIS (SETS)")
    print("="*60)

    generos_antigos = set()
    generos_novos   = set()

    for musica in musicas:
        campo_data   = musica.get('album_release_date', '') or musica.get('release_date', '')
        campo_genero = musica.get('artist_genres', '')

        ano = extrair_ano(campo_data)

        if ano == 0:
            continue

        generos_desta_musica = extrair_generos(campo_genero)

        if ano < 2015:
            generos_antigos |= generos_desta_musica
        elif ano >= 2024:
            generos_novos |= generos_desta_musica

    intersecao = generos_antigos & generos_novos
    sumidos    = generos_antigos - generos_novos
    novos      = generos_novos   - generos_antigos

    print(f"\n  Total de gêneros únicos antes de 2015 : {len(generos_antigos)}")
    print(f"  Total de gêneros únicos em 2024+      : {len(generos_novos)}")

    print(f"\n  🔁 INTERSEÇÃO — Gêneros que PERSISTIRAM ({len(intersecao)} gêneros):")
    _imprimir_em_colunas(sorted(intersecao), colunas=4)

    print(f"\n  ❌ GÊNEROS QUE SUMIRAM (antes‑2015 mas não em 2024+) — {len(sumidos)} gêneros:")
    _imprimir_em_colunas(sorted(sumidos), colunas=4)

    print(f"\n  ✅ GÊNEROS NOVOS (em 2024+ mas não antes de 2015) — {len(novos)} gêneros:")
    _imprimir_em_colunas(sorted(novos), colunas=4)

    print()

def _imprimir_em_colunas(lista: list, colunas: int = 4) -> None:
    """Função auxiliar: imprime uma lista em múltiplas colunas para facilitar leitura."""
    if not lista:
        print("    (nenhum resultado encontrado)")
        return

    # List Comprehension que monta cada linha com 'colunas' itens formatados
    for i in range(0, len(lista), colunas):
        linha = lista[i:i + colunas]   # Fatiamento: pega 'colunas' itens por vez
        # Cada item é justificado à esquerda em 28 caracteres para alinhar colunas
        print("    " + "".join(f"{item:<28}" for item in linha))

# opção 5: grádico de barras: top 10 músicas mais populares
def grafico_barras_top10(musicas: list) -> None:
    print("\n" + "="*60)
    print("  OPÇÃO 5 — GRÁFICO DE BARRAS: TOP 10 MAIS POPULARES")
    print("="*60)

    dados_validos = []
    for m in musicas:
        if m.get('track_popularity', '').strip() and _eh_numero(m.get('track_popularity', '')):
            tupla = (
                int(float(m['track_popularity'])),
                m.get('track_name', 'Desconhecida').strip(),
                m.get('artist_name', 'Desconhecido').strip()
            )
            dados_validos.append(tupla)

    dados_validos.sort(key=lambda t: t[0], reverse=True)

    vistos = set()
    top10  = []
    for popularidade, nome, artista in dados_validos:
        if nome not in vistos:
            vistos.add(nome)
            top10.append((popularidade, nome, artista))
        if len(top10) == 10:
            break

    popularidades = []
    nomes = []
    for t in top10:
        popularidades.append(t[0])
        nomes.append(f"{t[1][:30]}\n({t[2][:20]})")


    barra = go.Bar(
        x=nomes,
        y=popularidades,
        marker=dict(
            color=popularidades,
            colorscale='Viridis',
            showscale=True,
            line=dict(color='white', width=0.5)
        ),
        text=popularidades,
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Popularidade: %{y}<extra></extra>'
    )

    layout = go.Layout(
        title=dict(text='🎵 Top 10 Músicas Mais Populares no Spotify', font=dict(size=20)),
        xaxis=dict(title='Música (Artista)', tickangle=-15),
        yaxis=dict(title='Popularidade', range=[0, 105]),
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#ffffff',
        showlegend=False
    )

    figura = go.Figure(data=[barra], layout=layout)
    figura.show()
    print("\n  [OK] Gráfico aberto no navegador!\n")

# opção 6: scatter plot: popularidade do artista vs da música
def scatter_popularidade(musicas: list) -> None:
    print("\n" + "="*60)
    print("  OPÇÃO 6 — SCATTER PLOT: POPULARIDADE ARTISTA vs MÚSICA")
    print("="*60)

    dados = []
    for m in musicas:
        tem_artist = m.get('artist_popularity', '').strip() and _eh_numero(m.get('artist_popularity', ''))
        tem_track  = m.get('track_popularity',  '').strip() and _eh_numero(m.get('track_popularity',  ''))
        if tem_artist and tem_track:
            dados.append({
                'x':       float(m['artist_popularity']),
                'y':       float(m['track_popularity']),
                'nome':    m.get('track_name', '?').strip()[:40],
                'artista': m.get('artist_name', '?').strip()[:30],
                'explicit': m.get('explicit', 'FALSE').strip().upper() == 'TRUE'
            })

    explicitas     = []
    nao_explicitas = []
    for d in dados:
        if d['explicit']:
            explicitas.append(d)
        else:
            nao_explicitas.append(d)

    def criar_trace(grupo, nome_grupo, cor):
        # monta as listas ANTES
        x = []
        y = []
        customdata = []
        for d in grupo:
            x.append(d['x'])
            y.append(d['y'])
            customdata.append([d['nome'], d['artista']])

        # passa as listas prontas para o go.Scatter
        return go.Scatter(
            x    = x,
            y    = y,
            mode = 'markers',
            name = nome_grupo,
            marker=dict(
                color=cor,
                size=6,
                opacity=0.6,
                line=dict(width=0.3, color='white')
            ),
            hovertemplate=(
                '<b>%{customdata[0]}</b><br>'
                'Artista: %{customdata[1]}<br>'
                'Pop. Artista: %{x}<br>'
                'Pop. Música: %{y}'
                '<extra></extra>'
            ),
            customdata=customdata
        )

    trace_nao_explicitas = criar_trace(nao_explicitas, '🟢 Não‑Explícitas', '#1DB954')
    trace_explicitas     = criar_trace(explicitas,     '🔴 Explícitas',     '#E22134')

    layout = go.Layout(
        title=dict(text='🎯 Popularidade do Artista vs Popularidade da Música', font=dict(size=20)),
        xaxis=dict(title='Popularidade do Artista (0–100)', range=[-2, 102]),
        yaxis=dict(title='Popularidade da Música (0–100)',  range=[-2, 102]),
        plot_bgcolor='#f0f0f0',
        paper_bgcolor='#ffffff',
        legend=dict(x=0.01, y=0.99)
    )

    figura = go.Figure(data=[trace_nao_explicitas, trace_explicitas], layout=layout)
    figura.show()
    print("\n  [OK] Gráfico aberto no navegador!\n")

# menu interativo
def exibir_menu() -> None:
    print("\n" + "╔" + "═"*56 + "╗")
    print("║" + "   🎵  ANÁLISE DO DATASET SPOTIFY  🎵".center(56) + "║")
    print("╠" + "═"*56 + "╣")
    print("║  1. Top 10 Artistas com Mais Seguidores              ║")
    print("║  2. Top 15 Músicas Mais Longas                       ║")
    print("║  3. Popularidade Média: Explícitas vs Não‑Explícitas ║")
    print("║  4. Cruzamento de Gêneros (Sets)                     ║")
    print("║  5. Gráfico de Barras — Top 10 Mais Populares        ║")
    print("║  6. Scatter Plot — Popularidade Artista x Música     ║")
    print("║  0. Sair                                             ║")
    print("╚" + "═"*56 + "╝")
    print("  Escolha uma opção: ", end="")


def executar_menu(musicas: list) -> None:
    opcoes = {
        '1': lambda: top10_artistas_seguidores(musicas),
        '2': lambda: top15_musicas_mais_longas(musicas),
        '3': lambda: comparar_popularidade_explicitas(musicas),
        '4': lambda: cruzamento_generos_sets(musicas),
        '5': lambda: grafico_barras_top10(musicas),
        '6': lambda: scatter_popularidade(musicas),
    }

    while True:
        exibir_menu()
        escolha = input().strip()

        if escolha == '0':
            print("\n  Até logo! 👋\n")
            break
        elif escolha in opcoes:
            opcoes[escolha]()
            input("  Pressione ENTER para continuar...")
            os.system('cls')
        else:
            print("\n  [!] Opção inválida. Digite um número de 0 a 6.\n")

# ponto de entrada
if __name__ == "__main__":
    print("\n" + "="*60)
    print("  Carregando dados do dataset Spotify...")
    print("="*60)

    musicas = ler_dados(NOME_ARQUIVO)

    if musicas:
        executar_menu(musicas)
    else:
        print("  Programa encerrado por falta de dados.\n")