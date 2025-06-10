# Análise e Visualização das Copas do Mundo de Futebol

## 1. Tema do Projeto

Visualização e análise exploratória das Copas do Mundo de Futebol utilizando dados históricos oficiais.  
O objetivo é explorar estatísticas dos torneios, partidas e jogadores, através de dashboards interativos com filtros para melhor compreensão dos dados.

---

## 2. URL do Repositório no GitHub

O código e os arquivos do projeto estão hospedados no seguinte repositório GitHub:  
[# Análise e Visualização das Copas do Mundo de Futebol

## 1. Tema do Projeto

Visualização e análise exploratória das Copas do Mundo de Futebol utilizando dados históricos oficiais.  
O objetivo é explorar estatísticas dos torneios, partidas e jogadores, através de dashboards interativos com filtros para melhor compreensão dos dados.

---

## 2. URL do Repositório no GitHub

O código e os arquivos do projeto estão hospedados no seguinte repositório GitHub:  
[https://github.com/SeuUsuario/seu-repositorio.git](https://github.com/SeuUsuario/seu-repositorio.git)  

**Obs.:** Para acesso, concedi permissão ao usuário `diegopatr` (diegoinacio@upf.br).

---

## 3. Dataset Utilizado

### Origem dos Dados

Foram utilizados os datasets públicos da FIFA sobre as Copas do Mundo, disponíveis no site Kaggle e outras fontes abertas:

- **WorldCups.csv** — informações gerais de cada edição do campeonato (país sede, número de times, público, gols, vencedor, etc).
- **WorldCupMatches.csv** — dados de cada partida (times, placar, fase, público, etc).
- **WorldCupPlayers.csv** — dados dos jogadores e seus eventos (gols, cartões, posições, etc).

### Variáveis Principais

- **WorldCups.csv:** Year, Country, Winner, Runners-Up, GoalsScored, Attendance, QualifiedTeams, etc.
- **WorldCupMatches.csv:** Year, Stage, Home Team Goals, Away Team Goals, Attendance, etc.
- **WorldCupPlayers.csv:** Player Name, Team Initials, Position, Event, Shirt Number, etc.

### Transformações Realizadas

- Limpeza dos nomes das colunas para remover espaços.
- Criação de colunas auxiliares, como `Total Goals` na base de partidas (soma dos gols de ambas equipes).
- Filtragens por país sede, fase da partida e time para análise segmentada.
- Geração de estatísticas descritivas para as três bases de dados.
- Exportação dos gráficos gerados para arquivos PNG para registro.

---

## 4. Modelos Utilizados ou Desenvolvidos

Este projeto tem caráter exploratório e visual. Portanto, não foram aplicados modelos preditivos ou classificatórios.  

O foco está na análise descritiva e visualização dos dados por meio de gráficos interativos, usando:

- **Dash** (framework web para dashboards interativos em Python)
- **Plotly Express** (biblioteca para geração de gráficos)
- **Pandas** (manipulação e tratamento dos dados)

---

## 5. Resultados Obtidos

- Criação de um dashboard interativo com três seções principais:
  - **Copas do Mundo:** gráficos de gols, público e distribuição de títulos por país.
  - **Partidas:** histogramas de gols por partida e boxplot de público por fase do torneio.
  - **Jogadores:** lista filtrável por time com informações e gráfico de eventos por posição.

- O app permite filtrar os dados por país sede, fase do jogo e time, facilitando a exploração dinâmica.

- Estatísticas descritivas consolidadas foram geradas e exportadas para análise posterior.

- Os gráficos são exportados automaticamente como imagens para facilitar documentação e apresentações.

---

## Contato

Para dúvidas ou acesso ao projeto, favor contatar Guilherme ou o usuário `diegopatr` no GitHub.
https://github.com/BeckerPF2021/DataScience-WordCup]

---

## 3. Dataset Utilizado

### Origem dos Dados

Foram utilizados os datasets públicos da FIFA sobre as Copas do Mundo, disponíveis no site Kaggle e outras fontes abertas:

- **WorldCups.csv** — informações gerais de cada edição do campeonato (país sede, número de times, público, gols, vencedor, etc).
- **WorldCupMatches.csv** — dados de cada partida (times, placar, fase, público, etc).
- **WorldCupPlayers.csv** — dados dos jogadores e seus eventos (gols, cartões, posições, etc).

### Variáveis Principais

- **WorldCups.csv:** Year, Country, Winner, Runners-Up, GoalsScored, Attendance, QualifiedTeams, etc.
- **WorldCupMatches.csv:** Year, Stage, Home Team Goals, Away Team Goals, Attendance, etc.
- **WorldCupPlayers.csv:** Player Name, Team Initials, Position, Event, Shirt Number, etc.

### Transformações Realizadas

- Limpeza dos nomes das colunas para remover espaços.
- Criação de colunas auxiliares, como `Total Goals` na base de partidas (soma dos gols de ambas equipes).
- Filtragens por país sede, fase da partida e time para análise segmentada.
- Geração de estatísticas descritivas para as três bases de dados.
- Exportação dos gráficos gerados para arquivos PNG para registro.

---

## 4. Modelos Utilizados ou Desenvolvidos

Este projeto tem caráter exploratório e visual. Portanto, não foram aplicados modelos preditivos ou classificatórios.  

O foco está na análise descritiva e visualização dos dados por meio de gráficos interativos, usando:

- **Dash** (framework web para dashboards interativos em Python)
- **Plotly Express** (biblioteca para geração de gráficos)
- **Pandas** (manipulação e tratamento dos dados)

---

## 5. Resultados Obtidos

- Criação de um dashboard interativo com três seções principais:
  - **Copas do Mundo:** gráficos de gols, público e distribuição de títulos por país.
  - **Partidas:** histogramas de gols por partida e boxplot de público por fase do torneio.
  - **Jogadores:** lista filtrável por time com informações e gráfico de eventos por posição.

- O app permite filtrar os dados por país sede, fase do jogo e time, facilitando a exploração dinâmica.

- Estatísticas descritivas consolidadas foram geradas e exportadas para análise posterior.

- Os gráficos são exportados automaticamente como imagens para facilitar documentação e apresentações.

![Dashboard do Projeto](images/Dashboard.png)