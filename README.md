# 🏆 Análise e Visualização das Copas do Mundo de Futebol

Este projeto apresenta uma análise exploratória, visualização interativa e predição de dados históricos das Copas do Mundo de Futebol, utilizando bibliotecas de ciência de dados e ferramentas de visualização modernas. O objetivo é tornar o processo de análise intuitivo, interativo e acessível por meio de dashboards web dinâmicos.

---

## 📁 Estrutura do Projeto

- `data/` — arquivos CSV com dados históricos das Copas.
- `plots/` — gráficos gerados automaticamente para análise.
- `output/` — estatísticas descritivas exportadas.
- `images/` — imagens utilizadas no dashboard (ex: Dashboard.png).
- `app.py` — inicialização da aplicação Dash com layout e rotas.
- `data_loader.py` — funções para carregar e preparar os dados.
- `visualization.py` — criação de gráficos com Plotly.
- `callbacks.py` — lógica interativa dos componentes da interface.
- `ml_model.py` — treinamento e visualização dos modelos de regressão.
- `utils.py` — funções auxiliares (formatação, validação, mapeamentos).
- `constants.py` — dicionários e constantes globais utilizadas no projeto.
- `README.md` — este documento.
- `requirements.txt` — bibliotecas necessárias para execução.

---

## 🌐 Acesse o Projeto

Repositório no GitHub:  
[github.com/BeckerPF2021/DataScience-WordCup](https://github.com/BeckerPF2021/DataScience-WordCup)

---

## 📊 Datasets

Os dados foram obtidos de fontes públicas como a FIFA e o Kaggle:

- `WorldCups.csv` — informações por edição (ano, país, vencedor, público etc.)
- `WorldCupMatches.csv` — dados por partida (gols, fase, público)
- `WorldCupPlayers.csv` — informações sobre os jogadores e eventos (posição, cartões, gols)

### Transformações Realizadas

- Padronização de colunas e tipos de dados.
- Criação de métricas auxiliares como `Total Goals`.
- Filtros dinâmicos aplicados por país, fase, time e ano.
- Exportação de estatísticas descritivas e gráficos para `.csv` e `.png`.

---

## 🧪 Tecnologias e Ferramentas

- **Dash**: construção de dashboards web.
- **Plotly**: visualizações interativas.
- **Pandas & NumPy**: manipulação e análise de dados.
- **Scikit-learn**: modelo de regressão linear e métricas de performance.

---

## 🤖 Modelo Preditivo

Modelo de regressão linear implementado para prever:

- Total de público por Copa.
- Média de público por partida.
- Total de gols por edição.

### Resultados:

- Predições para edições futuras.
- Métricas de desempenho (R², RMSE).
- Classificação da performance (Excelente, Boa, Regular, Baixa).
- Gráficos de tendência e comparação real vs predito.

---

## 📈 Dashboard Interativo

Dividido em 5 seções:

1. **Visão Geral**: gols, público e títulos.
2. **Partidas**: distribuição por fase.
3. **Jogadores**: eventos e posições.
4. **Correlação entre Datasets**.
5. **Predições com Machine Learning**.

Com filtros por país, fase, time e edição.

![Dashboard do Projeto](images/Dashboard.png)

---

## 📬 Contato

Desenvolvido por **Guilherme Becker**  
📧 Email: `guilhermepf97@live.com`  
🔗 GitHub: [github.com/BeckerPF2021](https://github.com/BeckerPF2021/DataScience-WordCup)

---

Sinta-se à vontade para clonar, contribuir ou sugerir melhorias. ⚽📊🚀