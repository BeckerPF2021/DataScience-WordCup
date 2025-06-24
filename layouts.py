from dash import dcc, html

# Estilo reutilizável para dropdowns
dropdown_style = {'width': '100%', 'padding': '8px', 'marginBottom': '20px'}

def get_cups_layout(df_cups):
    return html.Div([
        html.H3("🏟️ Análise por País-Sede", style={'textAlign': 'center', 'marginBottom': '30px'}),
        dcc.Dropdown(
            id='dropdown-host',
            options=[{'label': c, 'value': c} for c in sorted(df_cups['Country'].unique())],
            placeholder="Selecione um país-sede",
            clearable=True,
            style=dropdown_style
        ),
        html.Div([
            dcc.Graph(id='graph-goals', style={'marginBottom': '40px'}),
            dcc.Graph(id='graph-attendance', style={'marginBottom': '40px'}),
            dcc.Graph(id='graph-titles')
        ])
    ], style={'padding': '20px', 'maxWidth': '1000px', 'margin': 'auto'})


def get_matches_layout(df_matches):
    return html.Div([
        html.H3("⚽ Análise de Partidas por Fase", style={'textAlign': 'center', 'marginBottom': '30px'}),
        dcc.Dropdown(
            id='dropdown-stage',
            options=[{'label': s, 'value': s} for s in sorted(df_matches['Stage'].unique())],
            placeholder="Selecione uma fase",
            clearable=True,
            style=dropdown_style
        ),
        dcc.Graph(id='graph-match-goals', style={'marginBottom': '40px'}),
        dcc.Graph(id='graph-attendance-matches')
    ], style={'padding': '20px', 'maxWidth': '1000px', 'margin': 'auto'})


def get_players_layout(df_players):
    return html.Div([
        html.H3("👥 Estatísticas de Jogadores", style={'textAlign': 'center', 'marginBottom': '30px'}),
        dcc.Dropdown(
            id='dropdown-team',
            options=[{'label': t, 'value': t} for t in sorted(df_players['Team Initials'].unique())],
            placeholder="Selecione um time",
            clearable=True,
            style=dropdown_style
        ),
        html.Div(id='players-list', style={'marginBottom': '40px'}),
        dcc.Graph(id='graph-events')
    ], style={'padding': '20px', 'maxWidth': '1000px', 'margin': 'auto'})


def get_relacao_layout(df_cups):
    return html.Div([
        html.H3("📊 Relação entre Edições", style={'textAlign': 'center', 'marginBottom': '30px'}),
        dcc.Dropdown(
            id='dropdown-year',
            options=[{'label': int(y), 'value': int(y)} for y in sorted(df_cups['Year'].unique())],
            placeholder="Selecione um ano",
            clearable=True,
            style=dropdown_style
        ),
        dcc.Graph(id='graph-edition-matches', style={'marginBottom': '40px'}),
        dcc.Graph(id='graph-edition-cups', style={'marginBottom': '40px'}),
        dcc.Graph(id='graph-goals-correlation')
    ], style={'padding': '20px', 'maxWidth': '1000px', 'margin': 'auto'})


def get_ml_layout():
    return html.Div([
        html.H2("🤖 Machine Learning - Predição de Público", style={
            'textAlign': 'center', 'color': '#d32f2f', 'marginBottom': '30px'
        }),
        html.Div([
            html.Div([
                html.Label("Ano para Predição:"),
                dcc.Input(
                    id='prediction-year',
                    type='number',
                    value=2030,
                    min=2025,
                    max=2050,
                    step=1,
                    style=dropdown_style
                ),
            ], style={'width': '48%', 'display': 'inline-block'}),
            html.Div([
                html.Label("Tipo de Predição:"),
                dcc.Dropdown(
                    id='prediction-type',
                    options=[
                        {'label': 'Público Total da Copa', 'value': 'total_attendance'},
                        {'label': 'Média de Público por Partida', 'value': 'avg_attendance'},
                        {'label': 'Número de Gols', 'value': 'goals'}
                    ],
                    value='total_attendance',
                    clearable=False,
                    style=dropdown_style
                ),
            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
        ], style={'marginBottom': '30px'}),
        html.Div(id='ml-results', style={'marginBottom': '30px'}),
        dcc.Graph(id='ml-prediction-graph', style={'marginBottom': '40px'}),
        dcc.Graph(id='ml-model-performance')
    ], style={'padding': '20px', 'maxWidth': '1000px', 'margin': 'auto'})


def get_main_layout():
    return html.Div([
        html.H1("🏆 FIFA - Copas do Mundo", style={
            'textAlign': 'center', 'color': '#0d47a1',
            'marginBottom': '40px', 'fontSize': '36px', 'fontWeight': 'bold'
        }),
        html.Div([
            html.Button("Copas do Mundo", id="btn-cups", n_clicks=0, className="menu-btn"),
            html.Button("Partidas", id="btn-matches", n_clicks=0, className="menu-btn"),
            html.Button("Jogadores", id="btn-players", n_clicks=0, className="menu-btn"),
            html.Button("Relação CSVs", id="btn-relacao", n_clicks=0, className="menu-btn"),
            html.Button("Machine Learning", id="btn-ml", n_clicks=0, className="menu-btn"),
        ], style={
            'textAlign': 'center', 'marginBottom': '30px', 'gap': '10px',
            'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'center'
        }),
        html.Div(id='page-content', style={'maxWidth': '1200px', 'margin': 'auto'})
    ])
