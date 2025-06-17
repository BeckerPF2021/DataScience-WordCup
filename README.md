# Análise e Visualização das Copas do Mundo de Futebol

## 1. Tema do Projeto

Visualização, análise exploratória e predição sobre as Copas do Mundo de Futebol utilizando dados históricos oficiais.  
O objetivo é explorar estatísticas dos torneios, partidas e jogadores, além de prever tendências futuras com modelos de Machine Learning. Tudo isso por meio de dashboards interativos com filtros dinâmicos que facilitam a navegação e análise.

![Dashboard do Projeto](images/Dashboard.png)

---

## 2. URL do Repositório no GitHub

O código e os arquivos do projeto estão hospedados no seguinte repositório GitHub:  
[https://github.com/BeckerPF2021/DataScience-WordCup](https://github.com/BeckerPF2021/DataScience-WordCup)

---

## 3. Dataset Utilizado

### Origem dos Dados

Foram utilizados datasets públicos da FIFA sobre as Copas do Mundo, obtidos no Kaggle e fontes abertas:

- **WorldCups.csv** — informações gerais por edição (ano, país sede, vencedor, gols, público, etc).
- **WorldCupMatches.csv** — informações detalhadas por partida (fase, gols, público, etc).
- **WorldCupPlayers.csv** — dados de jogadores e eventos ocorridos (posição, gols, cartões, etc).

### Variáveis Principais

- **WorldCups.csv:** `Year`, `Country`, `Winner`, `Runners-Up`, `GoalsScored`, `Attendance`, `QualifiedTeams`.
- **WorldCupMatches.csv:** `Year`, `Stage`, `Home Team Goals`, `Away Team Goals`, `Attendance`.
- **WorldCupPlayers.csv:** `Player Name`, `Team Initials`, `Position`, `Event`, `Shirt Number`.

### Transformações Realizadas

- Padronização dos nomes das colunas.
- Conversão de colunas numéricas para o tipo adequado.
- Criação de variáveis auxiliares como `Total Goals`.
- Filtragens por país sede, fase e time.
- Geração de estatísticas descritivas para todos os datasets.
- Exportação automática de gráficos para imagens PNG.

---

## 4. Tecnologias e Modelos Utilizados

### Bibliotecas e Frameworks

- **Dash:** construção de dashboard web com múltiplas páginas e callbacks reativos.
- **Plotly Express & Graph Objects:** visualizações interativas.
- **Pandas e NumPy:** tratamento de dados.
- **Scikit-learn:** regressão linear e métricas de performance para predição.

### Modelos de Machine Learning

Foi implementado um **modelo de Regressão Linear** para prever:

- Público total por Copa.
- Média de público por partida.
- Quantidade total de gols.

O modelo é treinado com as edições anteriores e retorna:

- Predição para ano futuro.
- Métricas de desempenho (R², RMSE).
- Classificação da qualidade do modelo (Excelente, Boa, Regular, Baixa).
- Gráficos de tendência e comparação real vs predito.

---

## 5. Resultados Obtidos

- **Dashboard completo** com 5 seções:
  - **Copas do Mundo:** gráfico de gols, público total e títulos por país.
  - **Partidas:** distribuição de gols e público por fase do torneio.
  - **Jogadores:** listagem e gráfico de eventos por posição com filtro por time.
  - **Relação entre Datasets:** correlação entre métricas das edições.
  - **Machine Learning:** predição para futuras edições com gráficos interativos e análise de performance.

- **Filtros dinâmicos** permitem análises segmentadas por país sede, fase da competição, time ou ano.

- **Estatísticas descritivas** exportadas para análise posterior em `output/descriptive_stats.csv`.

- **Gráficos salvos automaticamente** em `plots/`, permitindo uso em relatórios e apresentações.

---

## 6. Contato

Para dúvidas ou sugestões, entre em contato com Guilherme:  
📧 `guilhermepf97@live.com`  
🔗 GitHub: [https://github.com/BeckerPF2021/DataScience-WordCup](https://github.com/BeckerPF2021/DataScience-WordCup)