# 🎵 Spotify Data Analysis

Sistema de análise de dados do Spotify desenvolvido em Python utilizando estruturas de dados fundamentais como:

- Listas
- Dicionários
- Conjuntos (`set`)
- Tuplas

O projeto realiza análises estatísticas e comparações utilizando um dataset real do Spotify, além de gerar gráficos interativos com Plotly.

> Trabalho acadêmico da disciplina de Algoritmos e Estruturas de Dados.

---

# 📌 Objetivo do Projeto

O objetivo do projeto é aplicar conceitos de:

- Manipulação de arquivos CSV
- Estruturas de dados
- Ordenação e agrupamento
- Operações com conjuntos
- Visualização de dados
- Organização de código em funções

Tudo utilizando Python puro.

---

# 🛠️ Tecnologias Utilizadas

| Tecnologia | Função |
|---|---|
| Python 3 | Linguagem principal |
| `csv` | Leitura do dataset |
| `os` | Manipulação do sistema operacional |
| Plotly | Criação de gráficos interativos |

---

# 📂 Dataset Utilizado

Dataset do Spotify contendo informações como:

- Nome da música
- Artista
- Popularidade
- Seguidores
- Duração
- Data de lançamento
- Gêneros musicais
- Conteúdo explícito

Arquivo utilizado:

```text
spotify_data clean.csv
```

https://www.kaggle.com/datasets/wardabilal/spotify-global-music-dataset-20092025

---

# 🚀 Funcionalidades

## 📊 Análises de Dados

### ✅ Top 10 artistas com mais seguidores

- Agrupamento com dicionários
- Ordenação decrescente
- Ranking dos artistas mais populares

---

### ✅ Top 15 músicas mais longas

- Ordenação por duração
- Uso de listas e tuplas
- Exibição formatada

---

### ✅ Comparação de popularidade

Comparação entre:

- músicas explícitas
- músicas não explícitas

Calculando:
- quantidade
- média de popularidade

---

### ✅ Cruzamento de gêneros musicais com Sets

Operações de conjuntos:

- interseção
- diferença
- identificação de gêneros persistentes
- gêneros novos
- gêneros que desapareceram

---

# 📈 Visualizações Gráficas

## 🎯 Gráfico de Barras

Top 10 músicas mais populares do dataset.

Recursos:
- escala de cores
- labels
- hover interativo

---

## 🎯 Scatter Plot

Comparação entre:

- popularidade do artista
- popularidade da música

Separando:
- músicas explícitas
- músicas não explícitas

---

# 🧠 Estruturas de Dados Aplicadas

| Estrutura | Aplicação |
|---|---|
| Lista | Armazenamento principal das músicas |
| Dicionário | Agrupamento de informações |
| Set | Operações matemáticas entre gêneros |
| Tupla | Organização de dados para ordenação |

---

# ⚙️ Como Executar

## 1️⃣ Clone o repositório

```bash
git clone https://github.com/leonardorosler/spotify-data-analysis.git
```

---

## 2️⃣ Entre na pasta

```bash
cd spotify-data-analysis
```

---

## 3️⃣ Instale as dependências

```bash
pip install plotly
```

---

## 4️⃣ Execute o programa

```bash
python main.py
```

> O arquivo `spotify_data clean.csv` deve estar na mesma pasta do script principal.

---

# 🖥️ Menu Interativo

O sistema funciona através de um menu no terminal:

```text
1. Top 10 Artistas com Mais Seguidores
2. Top 15 Músicas Mais Longas
3. Popularidade Média: Explícitas vs Não-Explícitas
4. Cruzamento de Gêneros (Sets)
5. Gráfico de Barras — Top 10 Mais Populares
6. Scatter Plot — Popularidade Artista x Música
0. Sair
```

---

# 📚 Conceitos Aplicados

## Estruturas de Dados

- Listas
- Dicionários
- Sets
- Tuplas

## Algoritmos

- Ordenação
- Agrupamento
- Filtragem
- Busca
- Operações matemáticas com conjuntos

## Manipulação de Dados

- Parsing de strings
- Tratamento de dados inválidos
- Conversão de tipos
- Limpeza de dados

## Visualização de Dados

- Gráfico de Barras
- Scatter Plot interativo

---

# 🧹 Tratamento de Dados

O dataset possui dados inconsistentes e valores vazios.

O sistema utiliza:
- validações
- `try/except`
- parsing de strings
- limpeza de dados

Para garantir estabilidade durante a execução.

---

# 📸 Exemplo de Saída

```text
Pos   Artista                             Seguidores
---------------------------------------------------------
1     Taylor Swift                        120,000,000
2     Drake                                95,000,000
3     The Weeknd                           91,000,000
```

---

# 🎓 Finalidade Acadêmica

Projeto desenvolvido para aplicação prática dos conteúdos da disciplina:

- Algoritmos e Estruturas de Dados
- Manipulação de estruturas em Python
- Geração de gráficos
- Organização de código
- Análise de datasets reais

---

# 👨‍💻 Autor

Desenvolvido por 