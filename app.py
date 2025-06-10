import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# --- Criar pastas output/ e plots/ caso não existam ---
os.makedirs('output', exist_ok=True)
os.makedirs('plots', exist_ok=True)

# --- Carregar dados ---
df_cups = pd.read_csv("data/WorldCups.csv")
df_cups.columns = df_cups.columns.str.strip()

df_matches = pd.read_csv("data/WorldCupMatches.csv")
df_matches.columns = df_matches.columns.str.strip()

df_players = pd.read_csv("data/WorldCupPlayers.csv")
df_players.columns = df_players.columns.str.strip()

# --- Gerar e salvar estatísticas descritivas ---
def save_descriptive_stats():
    stats_cups = df_cups.describe(include='all').transpose()
    stats_cups['dataset'] = 'WorldCups'

    stats_matches = df_matches.describe(include='all').transpose()
    stats_matches['dataset'] = 'WorldCupMatches'

    stats_players = df_players.describe(include='all').transpose()
    stats_players['dataset'] = 'WorldCupPlayers'

    all_stats = pd.concat([stats_cups, stats_matches, stats_players])
    all_stats.to_csv('output/descriptive_stats.csv')

save_descriptive_stats()

# --- Função para salvar gráficos na pasta plots, com prints e tratamento de erro ---
def save_figure(fig, filename):
    abs_path = os.path.abspath(os.path.join('plots', filename))
    print(f"Tentando salvar figura em: {abs_path}")
    try:
        fig.write_image(abs_path)
        print("Imagem salva com sucesso.")
    except Exception as e:
        print(f"Erro ao salvar figura: {e}")

# --- Inicializa o app ---
app = dash.Dash(__name__)
app.title = "FIFA - Copas do Mundo"
app.config.suppress_callback_exceptions = True  # Corrige erro de ID not found in layout

# --- Layouts internos ---
cups_layout = html.Div([
    html.Label("Filtrar por País-Sede:"),
    dcc.Dropdown(
        id='dropdown-host',
        options=[{'label': c, 'value': c} for c in sorted(df_cups['Country'].unique())],
        placeholder="Selecione um país-sede",
        clearable=True
    ),
    dcc.Graph(id='graph-goals'),
    dcc.Graph(id='graph-attendance'),
    dcc.Graph(id='graph-titles'),
])

matches_layout = html.Div([
    html.Label("Filtrar por Fase do Jogo:"),
    dcc.Dropdown(
        id='dropdown-stage',
        options=[{'label': s, 'value': s} for s in sorted(df_matches['Stage'].dropna().unique())],
        placeholder="Selecione uma fase",
        clearable=True
    ),
    dcc.Graph(id='graph-match-goals'),
    dcc.Graph(id='graph-attendance-matches'),
])

# --- Menu jogadores aprimorado ---
if 'Team Name' in df_players.columns:
    team_options = [
        {'label': f"{row['Team Initials']} - {row['Team Name']}", 'value': row['Team Initials']}
        for _, row in df_players[['Team Initials', 'Team Name']].drop_duplicates().sort_values('Team Initials').iterrows()
    ]
else:
    team_options = [
        {'label': t, 'value': t}
        for t in sorted(df_players['Team Initials'].dropna().unique())
    ]

players_layout = html.Div([
    html.Label("Filtrar por Time:"),
    dcc.Dropdown(
        id='dropdown-team',
        options=team_options,
        placeholder="Selecione um time",
        clearable=True
    ),
    html.Div(id='players-list'),
    dcc.Graph(id='graph-events'),
])

# --- Layout principal com três botões para alternar ---
app.layout = html.Div([
    html.H1("FIFA - Copas do Mundo", style={'textAlign': 'center', 'color': '#0d47a1', 'marginBottom': '40px'}),

    html.Div([
        html.Button("Copas do Mundo", id="btn-cups", n_clicks=0, style={'marginRight': '10px'}),
        html.Button("Partidas", id="btn-matches", n_clicks=0, style={'marginRight': '10px'}),
        html.Button("Jogadores", id="btn-players", n_clicks=0)
    ], style={'textAlign': 'center', 'marginBottom': '30px'}),

    html.Div(id='page-content', style={'maxWidth': '1200px', 'margin': 'auto'})
])

# --- Callbacks de navegação ---
@app.callback(
    Output('page-content', 'children'),
    Input('btn-cups', 'n_clicks'),
    Input('btn-matches', 'n_clicks'),
    Input('btn-players', 'n_clicks'),
)
def display_page(n_cups, n_matches, n_players):
    # Mostra Copas ao abrir
    if not n_cups and not n_matches and not n_players:
        return cups_layout
    if n_players > n_cups and n_players > n_matches:
        return players_layout
    elif n_matches > n_cups:
        return matches_layout
    else:
        return cups_layout

# --- Callbacks Copas do Mundo ---
@app.callback(
    Output('graph-goals', 'figure'),
    Input('dropdown-host', 'value')
)
def update_goals_graph(selected_host):
    filtered_df = df_cups[df_cups['Country'] == selected_host] if selected_host else df_cups
    fig = px.bar(
        filtered_df,
        x='Year',
        y='GoalsScored',
        color='Country',
        title='Gols por Copa do Mundo',
        labels={'GoalsScored': 'Gols Marcados'},
        hover_data=['Winner', 'Runners-Up', 'QualifiedTeams']
    )
    fig.update_layout(transition_duration=500)
    save_figure(fig, 'goals_cups.png')
    return fig

@app.callback(
    Output('graph-attendance', 'figure'),
    Input('dropdown-host', 'value')
)
def update_attendance_graph(selected_host):
    filtered_df = df_cups[df_cups['Country'] == selected_host] if selected_host else df_cups
    fig = px.line(
        filtered_df,
        x='Year',
        y='Attendance',
        title='Público por Copa do Mundo',
        markers=True,
        labels={'Attendance': 'Público Total'}
    )
    fig.update_layout(transition_duration=500)
    save_figure(fig, 'attendance_cups.png')
    return fig

@app.callback(
    Output('graph-titles', 'figure'),
    Input('dropdown-host', 'value')
)
def update_titles_pie(selected_host):
    filtered_df = df_cups[df_cups['Country'] == selected_host] if selected_host else df_cups
    titles = filtered_df['Winner'].value_counts().reset_index()
    titles.columns = ['Country', 'Titles']
    fig = px.pie(
        titles,
        values='Titles',
        names='Country',
        title='Distribuição de Títulos por País',
        hole=0.4
    )
    fig.update_layout(transition_duration=500)
    save_figure(fig, 'titles_pie.png')
    return fig

# --- Callbacks Partidas ---
@app.callback(
    Output('graph-match-goals', 'figure'),
    Input('dropdown-stage', 'value')
)
def update_match_goals(stage):
    filtered_df = df_matches[df_matches['Stage'] == stage] if stage else df_matches
    filtered_df = filtered_df.copy()
    filtered_df['Total Goals'] = filtered_df['Home Team Goals'] + filtered_df['Away Team Goals']
    fig = px.histogram(
        filtered_df,
        x='Total Goals',
        nbins=15,
        title='Distribuição de Gols por Partida',
        labels={'Total Goals': 'Total de Gols na Partida'}
    )
    fig.update_layout(transition_duration=500)
    save_figure(fig, 'match_goals_histogram.png')
    return fig

@app.callback(
    Output('graph-attendance-matches', 'figure'),
    Input('dropdown-stage', 'value')
)
def update_match_attendance(stage):
    filtered_df = df_matches[df_matches['Stage'] == stage] if stage else df_matches
    fig = px.box(
        filtered_df,
        y='Attendance',
        title='Distribuição de Público por Fase',
        labels={'Attendance': 'Público'},
        points='all'
    )
    fig.update_layout(transition_duration=500)
    save_figure(fig, 'match_attendance_box.png')
    return fig

# --- Callbacks Jogadores ---
@app.callback(
    Output('players-list', 'children'),
    Output('graph-events', 'figure'),
    Input('dropdown-team', 'value')
)
def update_players_and_events(team_initials):
    filtered_df = df_players[df_players['Team Initials'] == team_initials] if team_initials else df_players

    # Lista de jogadores
    if filtered_df.empty:
        players_table = html.P("Nenhum jogador encontrado para este time.")
    else:
        players_table = html.Table(
            # Cabeçalho
            [html.Tr([html.Th(col) for col in ['Player Name', 'Position', 'Shirt Number', 'Event']])] +
            # Dados
            [html.Tr([
                html.Td(row['Player Name']),
                html.Td(row['Position']),
                html.Td(row['Shirt Number']),
                html.Td(row['Event']),
            ]) for _, row in filtered_df.iterrows()],
            style={'margin': 'auto', 'width': '80%', 'borderCollapse': 'collapse', 'boxShadow': '0 0 10px rgba(0,0,0,0.1)'}
        )

    # Gráfico de eventos por posição (contagem simples)
    event_counts = filtered_df.groupby('Position')['Event'].count().reset_index()
    fig = px.bar(
        event_counts,
        x='Position',
        y='Event',
        title='Eventos por Posição',
        labels={'Event': 'Número de Eventos'}
    )
    fig.update_layout(transition_duration=500)
    save_figure(fig, 'player_events_by_position.png')

    return players_table, fig

if __name__ == '__main__':
    app.run(debug=True)