import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# 1. Carregar dados e preparação
df = pd.read_csv("data/WorldCups.csv")
df.columns = df.columns.str.strip()
df = df.dropna(subset=['GoalsScored', 'Attendance', 'Winner'])

# Estatísticas descritivas para relatório
desc_stats = df.describe()
desc_stats.to_csv('output/descriptive_stats.csv')

# 2. Inicializar app Dash
app = dash.Dash(__name__)
app.title = "Dashboard FIFA - Copas do Mundo até 2018"

# 3. Layout
app.layout = html.Div([
    html.H1("Dashboard - Copas do Mundo FIFA até 2018", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Filtrar por País-Sede:"),
        dcc.Dropdown(
            id='dropdown-host',
            options=[{'label': c, 'value': c} for c in sorted(df['Country'].unique())],
            placeholder="Selecione um país-sede",
            clearable=True
        ),
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Br(),

    html.Div([dcc.Graph(id='graph-goals')]),
    html.Div([dcc.Graph(id='graph-attendance')]),
    html.Div([dcc.Graph(id='graph-titles')]),
])

# 4. Callbacks para atualizar gráficos dinamicamente

@app.callback(
    Output('graph-goals', 'figure'),
    Input('dropdown-host', 'value')
)
def update_goals_graph(selected_host):
    filtered_df = df[df['Country'] == selected_host] if selected_host else df
    fig = px.bar(
        filtered_df,
        x='Year',
        y='GoalsScored',
        color='Country',
        title='Gols por Copa do Mundo',
        labels={'GoalsScored': 'Gols Marcados'},
        hover_data=['Winner', 'Runners-Up', 'QualifiedTeams']
    )
    return fig

@app.callback(
    Output('graph-attendance', 'figure'),
    Input('dropdown-host', 'value')
)
def update_attendance_graph(selected_host):
    filtered_df = df[df['Country'] == selected_host] if selected_host else df
    fig = px.line(
        filtered_df,
        x='Year',
        y='Attendance',
        title='Público por Copa do Mundo',
        markers=True,
        labels={'Attendance': 'Público Total'}
    )
    return fig

@app.callback(
    Output('graph-titles', 'figure'),
    Input('dropdown-host', 'value')
)
def update_titles_pie(selected_host):
    filtered_df = df[df['Country'] == selected_host] if selected_host else df
    titles = filtered_df['Winner'].value_counts().reset_index()
    titles.columns = ['Country', 'Titles']
    fig = px.pie(
        titles,
        values='Titles',
        names='Country',
        title='Distribuição de Títulos por País',
        hole=0.4
    )
    return fig

if __name__ == '__main__':
    app.run(debug=True)