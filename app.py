import os
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

os.makedirs('output', exist_ok=True)
os.makedirs('plots', exist_ok=True)

def load_and_prepare_data():
    df_cups = pd.read_csv("data/WorldCups.csv")
    df_cups.columns = df_cups.columns.str.strip()
    required_cups_cols = ['Year', 'Country', 'Winner', 'Runners-Up', 'GoalsScored', 'Attendance', 'QualifiedTeams']
    assert all(col in df_cups.columns for col in required_cups_cols), "Colunas faltando em WorldCups.csv"
    df_cups = df_cups.dropna(subset=['Year', 'Country'])
    df_cups['Year'] = pd.to_numeric(df_cups['Year'], errors='coerce')
    df_cups['GoalsScored'] = pd.to_numeric(df_cups['GoalsScored'], errors='coerce')
    df_cups['Attendance'] = pd.to_numeric(df_cups['Attendance'], errors='coerce')
    df_cups['QualifiedTeams'] = pd.to_numeric(df_cups['QualifiedTeams'], errors='coerce')

    df_matches = pd.read_csv("data/WorldCupMatches.csv")
    df_matches.columns = df_matches.columns.str.strip()
    required_matches_cols = ['Year', 'Stage', 'Home Team Goals', 'Away Team Goals', 'Attendance']
    assert all(col in df_matches.columns for col in required_matches_cols), "Colunas faltando em WorldCupMatches.csv"
    df_matches = df_matches.dropna(subset=['Stage'])
    df_matches['Home Team Goals'] = pd.to_numeric(df_matches['Home Team Goals'], errors='coerce')
    df_matches['Away Team Goals'] = pd.to_numeric(df_matches['Away Team Goals'], errors='coerce')
    df_matches['Attendance'] = pd.to_numeric(df_matches['Attendance'], errors='coerce')

    df_players = pd.read_csv("data/WorldCupPlayers.csv")
    df_players.columns = df_players.columns.str.strip()
    required_players_cols = ['Player Name', 'Position', 'Shirt Number', 'Event', 'Team Initials']
    assert all(col in df_players.columns for col in required_players_cols), "Colunas faltando em WorldCupPlayers.csv"
    df_players = df_players.dropna(subset=['Player Name', 'Team Initials'])
    df_players['Shirt Number'] = pd.to_numeric(df_players['Shirt Number'], errors='coerce')

    return df_cups, df_matches, df_players

df_cups, df_matches, df_players = load_and_prepare_data()

def save_descriptive_stats():
    stats_cups = df_cups.describe(include='all').transpose(); stats_cups['dataset'] = 'WorldCups'
    stats_matches = df_matches.describe(include='all').transpose(); stats_matches['dataset'] = 'WorldCupMatches'
    stats_players = df_players.describe(include='all').transpose(); stats_players['dataset'] = 'WorldCupPlayers'
    pd.concat([stats_cups, stats_matches, stats_players]).to_csv('output/descriptive_stats.csv')

save_descriptive_stats()

def save_figure(fig, filename):
    path = os.path.join('plots', filename)
    try:
        fig.write_image(path)
    except:
        pass

app = dash.Dash(__name__)
app.title = "FIFA - Copas do Mundo"
app.config.suppress_callback_exceptions = True

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
        options=[{'label': s, 'value': s} for s in sorted(df_matches['Stage'].unique())],
        placeholder="Selecione uma fase",
        clearable=True
    ),
    dcc.Graph(id='graph-match-goals'),
    dcc.Graph(id='graph-attendance-matches'),
])

if 'Team Name' in df_players.columns:
    team_options = [{'label': f"{r['Team Initials']} - {r['Team Name']}", 'value': r['Team Initials']}
                    for _, r in df_players[['Team Initials','Team Name']].drop_duplicates().iterrows()]
else:
    team_options = [{'label': t, 'value': t} for t in sorted(df_players['Team Initials'].unique())]

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

relacao_layout = html.Div([
    html.Label("Filtrar por Edição (Ano):"),
    dcc.Dropdown(
        id='dropdown-year',
        options=[{'label': int(y), 'value': int(y)} for y in sorted(df_cups['Year'].unique())],
        placeholder="Selecione um ano",
        clearable=True
    ),
    dcc.Graph(id='graph-edition-matches'),
    dcc.Graph(id='graph-edition-cups'),
    dcc.Graph(id='graph-goals-correlation'),
], style={'padding': '20px'})

ml_layout = html.Div([
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
                style={'width': '100%', 'padding': '8px', 'marginBottom': '10px'}
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
                style={'marginBottom': '10px'}
            ),
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
    ], style={'marginBottom': '20px'}),
    
    html.Div(id='ml-results', style={'marginBottom': '20px'}),
    dcc.Graph(id='ml-prediction-graph'),
    dcc.Graph(id='ml-model-performance'),
    
], style={'padding': '20px'})

app.layout = html.Div([
    html.H1("🏆 FIFA - Copas do Mundo", style={
        'textAlign': 'center', 'color': '#0d47a1', 'marginBottom': '40px',
        'fontSize': '36px', 'fontWeight': 'bold', 'textShadow': '1px 1px #ccc'}),
    html.Div([
        html.Button("Copas do Mundo", id="btn-cups", n_clicks=0, style={
            'marginRight':'10px','padding':'12px 24px','backgroundColor':'#1976d2',
            'color':'white','border':'none','borderRadius':'8px','boxShadow':'2px 2px 5px rgba(0,0,0,0.2)'}),
        html.Button("Partidas", id="btn-matches", n_clicks=0, style={
            'marginRight':'10px','padding':'12px 24px','backgroundColor':'#388e3c',
            'color':'white','border':'none','borderRadius':'8px','boxShadow':'2px 2px 5px rgba(0,0,0,0.2)'}),
        html.Button("Jogadores", id="btn-players", n_clicks=0, style={
            'marginRight':'10px','padding':'12px 24px','backgroundColor':'#f57c00',
            'color':'white','border':'none','borderRadius':'8px','boxShadow':'2px 2px 5px rgba(0,0,0,0.2)'}),
        html.Button("Relação CSVs", id="btn-relacao", n_clicks=0, style={
            'marginRight':'10px','padding':'12px 24px','backgroundColor':'#6a1b9a',
            'color':'white','border':'none','borderRadius':'8px','boxShadow':'2px 2px 5px rgba(0,0,0,0.2)'}),
        html.Button("Machine Learning", id="btn-ml", n_clicks=0, style={
            'padding':'12px 24px','backgroundColor':'#d32f2f',
            'color':'white','border':'none','borderRadius':'8px','boxShadow':'2px 2px 5px rgba(0,0,0,0.2)'})
    ], style={'textAlign':'center','marginBottom':'30px'}),
    html.Div(id='page-content', style={
        'maxWidth':'1200px','margin':'auto','padding':'20px',
        'backgroundColor':'#f4f4f4','borderRadius':'12px','boxShadow':'0 4px 10px rgba(0,0,0,0.1)'})
])

@app.callback(
    Output('page-content','children'),
    Input('btn-cups','n_clicks'),
    Input('btn-matches','n_clicks'),
    Input('btn-players','n_clicks'),
    Input('btn-relacao','n_clicks'),
    Input('btn-ml','n_clicks')
)
def display_page(n1,n2,n3,n4,n5):
    if not any([n1,n2,n3,n4,n5]):
        return cups_layout
    mx = max(n1,n2,n3,n4,n5)
    if mx==n5: return ml_layout
    if mx==n4: return relacao_layout
    if mx==n3: return players_layout
    if mx==n2: return matches_layout
    return cups_layout

@app.callback(Output('graph-goals','figure'), Input('dropdown-host','value'))
def update_goals(selected):
    df = df_cups[df_cups['Country']==selected] if selected else df_cups
    fig = px.bar(df, x='Year', y='GoalsScored', color='Country',
                 title='Gols por Copa do Mundo',
                 labels={'GoalsScored':'Gols Marcados'},
                 hover_data=['Winner','Runners-Up','QualifiedTeams'])
    fig.update_layout(transition_duration=500)
    save_figure(fig,'goals_cups.png')
    return fig

@app.callback(Output('graph-attendance','figure'), Input('dropdown-host','value'))
def update_attendance(selected):
    df = df_cups[df_cups['Country']==selected] if selected else df_cups
    fig = px.line(df, x='Year', y='Attendance',
                  title='Público por Copa do Mundo', markers=True)
    fig.update_layout(transition_duration=500)
    save_figure(fig,'attendance_cups.png')
    return fig

@app.callback(Output('graph-titles','figure'), Input('dropdown-host','value'))
def update_titles(selected):
    df = df_cups[df_cups['Country']==selected] if selected else df_cups
    titles = df['Winner'].value_counts().reset_index()
    titles.columns = ['Country','Titles']
    fig = px.pie(titles, values='Titles', names='Country',
                 title='Distribuição de Títulos por País', hole=0.4)
    fig.update_layout(transition_duration=500)
    save_figure(fig,'titles_pie.png')
    return fig

@app.callback(Output('graph-match-goals','figure'), Input('dropdown-stage','value'))
def update_match_goals(stage):
    df = df_matches[df_matches['Stage']==stage].copy() if stage else df_matches.copy()
    df['Total Goals'] = df['Home Team Goals'] + df['Away Team Goals']
    fig = px.histogram(df, x='Total Goals', nbins=15,
                       title='Distribuição de Gols por Partida')
    fig.update_layout(transition_duration=500)
    save_figure(fig,'match_goals_histogram.png')
    return fig

@app.callback(Output('graph-attendance-matches','figure'), Input('dropdown-stage','value'))
def update_match_attendance(stage):
    df = df_matches[df_matches['Stage']==stage] if stage else df_matches
    fig = px.box(df, y='Attendance',
                 title='Distribuição de Público por Fase', points='all')
    fig.update_layout(transition_duration=500)
    save_figure(fig,'match_attendance_box.png')
    return fig

@app.callback(
    Output('players-list','children'),
    Output('graph-events','figure'),
    Input('dropdown-team','value')
)
def update_players_and_events(team):
    df = df_players[df_players['Team Initials']==team] if team else df_players
    if df.empty:
        table = html.P("Nenhum jogador encontrado para este time.")
    else:
        table = html.Table(
            [html.Tr([html.Th(c) for c in ['Player Name','Position','Shirt Number','Event']])] +
            [html.Tr([html.Td(r['Player Name']),html.Td(r['Position']),
                      html.Td(r['Shirt Number']),html.Td(r['Event'])])
             for _,r in df.iterrows()]
        )
    counts = df.groupby('Position')['Event'].count().reset_index()
    fig = px.bar(counts, x='Position', y='Event',
                 title='Eventos por Posição')
    fig.update_layout(transition_duration=500)
    save_figure(fig,'player_events_by_position.png')
    return table, fig

@app.callback(Output('graph-edition-matches','figure'), Input('dropdown-year','value'))
def update_edition_matches(year):
    dfm = df_matches[df_matches['Year']==year] if year else df_matches
    total = len(dfm)
    avg_g = (dfm['Home Team Goals']+dfm['Away Team Goals']).mean()
    avg_a = dfm['Attendance'].mean()
    dfm2 = pd.DataFrame({
        'Metric':['Total partidas','Média gols/jogo','Média público/jogo'],
        'Value':[total,avg_g,avg_a]
    })
    fig = px.bar(dfm2, x='Metric', y='Value',
                 title='Estatísticas de Partidas por Edição')
    return fig

@app.callback(Output('graph-edition-cups','figure'), Input('dropdown-year','value'))
def update_edition_cups(year):
    dfc = df_cups[df_cups['Year']==year] if year else df_cups
    g = dfc['GoalsScored'].iloc[0] if not dfc.empty else 0
    a = dfc['Attendance'].iloc[0] if not dfc.empty else 0
    t = dfc['QualifiedTeams'].iloc[0] if not dfc.empty else 0
    dfc2 = pd.DataFrame({
        'Metric':['Gols na edição','Público na edição','Times qualificados'],
        'Value':[g,a,t]
    })
    fig = px.bar(dfc2, x='Metric', y='Value',
                 title='Estatísticas da Edição')
    return fig

@app.callback(Output('graph-goals-correlation','figure'), Input('dropdown-year','value'))
def update_goals_correlation(year):
    dfa = df_matches.copy()
    dfa['TotalGoals'] = dfa['Home Team Goals']+dfa['Away Team Goals']
    summary = (dfa.groupby('Year')
                  .agg(avg_goals=('TotalGoals','mean'),
                       matches=('TotalGoals','size'))
                  .reset_index()
                  .merge(df_cups[['Year','GoalsScored','QualifiedTeams']], on='Year'))
    if year:
        summary = summary[summary['Year']==year]
    fig = px.scatter(summary, x='GoalsScored', y='avg_goals',
                     size='matches', hover_name=summary['Year'].astype(int),
                     title='Correlação: Gols na Edição × Média de Gols por Partida')
    return fig

# Callbacks para Machine Learning
@app.callback(
    Output('ml-results', 'children'),
    Output('ml-prediction-graph', 'figure'),
    Output('ml-model-performance', 'figure'),
    Input('prediction-year', 'value'),
    Input('prediction-type', 'value')
)
def update_ml_predictions(pred_year, pred_type):
    try:
        # Preparar dados baseado no tipo de predição
        if pred_type == 'total_attendance':
            df_ml = df_cups[['Year', 'Attendance']].dropna()
            target_col = 'Attendance'
            title = 'Predição de Público Total'
            y_label = 'Público Total'
        elif pred_type == 'avg_attendance':
            # Calcular média de público por partida
            avg_attendance = df_matches.groupby('Year')['Attendance'].mean().reset_index()
            df_ml = avg_attendance.dropna()
            target_col = 'Attendance'
            title = 'Predição de Público Médio por Partida'
            y_label = 'Público Médio'
        else:  # goals
            df_ml = df_cups[['Year', 'GoalsScored']].dropna()
            target_col = 'GoalsScored'
            title = 'Predição de Gols por Copa'
            y_label = 'Número de Gols'
        
        if len(df_ml) < 5:
            return html.P("Dados insuficientes para análise."), {}, {}
        
        # Preparar dados para ML
        X = df_ml[['Year']].values
        y = df_ml[target_col].values
        
        # Dividir dados em treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Treinar modelo
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        # Fazer predições
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)
        
        # Calcular métricas
        r2_train = r2_score(y_train, y_pred_train)
        r2_test = r2_score(y_test, y_pred_test)
        mse_test = mean_squared_error(y_test, y_pred_test)
        rmse_test = np.sqrt(mse_test)
        
        # Predição para o ano especificado
        future_pred = model.predict([[pred_year]])[0]
        
        # Interpretar qualidade do modelo
        if r2_test >= 0.8:
            quality = "🟢 Excelente"
            quality_color = "#4caf50"
        elif r2_test >= 0.6:
            quality = "🟡 Boa"
            quality_color = "#ff9800"
        elif r2_test >= 0.4:
            quality = "🟠 Regular"
            quality_color = "#ff5722"
        else:
            quality = "🔴 Baixa"
            quality_color = "#f44336"
        
        # Formatação melhor dos números
        if pred_type == 'total_attendance':
            pred_formatted = f"{future_pred:,.0f} pessoas"
            unit = "pessoas"
        elif pred_type == 'avg_attendance':
            pred_formatted = f"{future_pred:,.0f} pessoas por jogo"
            unit = "pessoas/jogo"
        else:
            pred_formatted = f"{future_pred:.0f} gols"
            unit = "gols"
        
        # Criar resultados mais claros
        results = html.Div([
            html.Div([
                html.H3("🔮 PREDIÇÃO", style={'margin': '0', 'color': '#1976d2'}),
                html.H2(f"{pred_year}: {pred_formatted}", style={
                    'margin': '5px 0', 'color': '#1976d2', 'fontSize': '28px'
                })
            ], style={
                'backgroundColor': '#e3f2fd', 'padding': '20px', 'borderRadius': '10px',
                'marginBottom': '15px', 'textAlign': 'center', 'border': '3px solid #1976d2'
            }),
            
            html.Div([
                html.Div([
                    html.H4("📊 QUALIDADE DO MODELO", style={'color': '#333', 'marginBottom': '10px'}),
                    html.H3(quality, style={'color': quality_color, 'fontSize': '24px', 'margin': '0'})
                ], style={'width': '48%', 'display': 'inline-block', 'textAlign': 'center'}),
                
                html.Div([
                    html.H4("🎯 PRECISÃO", style={'color': '#333', 'marginBottom': '10px'}),
                    html.H3(f"{r2_test*100:.1f}%", style={'color': quality_color, 'fontSize': '24px', 'margin': '0'})
                ], style={'width': '48%', 'display': 'inline-block', 'textAlign': 'center', 'float': 'right'})
            ], style={
                'backgroundColor': '#f5f5f5', 'padding': '15px', 'borderRadius': '8px',
                'marginBottom': '15px'
            }),
            
            html.Div([
                html.H4("📈 DETALHES TÉCNICOS", style={'color': '#666', 'marginBottom': '15px'}),
                html.Div([
                    html.Div([
                        html.Strong("Erro Médio: "),
                        f"{rmse_test:,.0f} {unit.split('/')[0] if '/' in unit else unit}"
                    ], style={'marginBottom': '8px'}),
                    html.Div([
                        html.Strong("Tendência Anual: "),
                        f"+{model.coef_[0]:,.0f} {unit.split('/')[0] if '/' in unit else unit} por ano" if model.coef_[0] > 0 else f"{model.coef_[0]:,.0f} {unit.split('/')[0] if '/' in unit else unit} por ano"
                    ], style={'marginBottom': '8px'}),
                    html.Div([
                        html.Strong("Dados Utilizados: "),
                        f"{len(df_ml)} Copas do Mundo ({df_ml['Year'].min()}-{df_ml['Year'].max()})"
                    ])
                ])
            ], style={
                'backgroundColor': '#fafafa', 'padding': '15px', 'borderRadius': '8px',
                'fontSize': '14px'
            })
        ])
        
        # Gráfico de predição
        years_extended = np.arange(df_ml['Year'].min(), pred_year + 5, 1)
        predictions_extended = model.predict(years_extended.reshape(-1, 1))
        
        fig_pred = go.Figure()
        
        # Dados históricos
        fig_pred.add_trace(go.Scatter(
            x=df_ml['Year'],
            y=df_ml[target_col],
            mode='markers',
            name='Dados Históricos',
            marker=dict(color='blue', size=8)
        ))
        
        # Linha de regressão
        fig_pred.add_trace(go.Scatter(
            x=years_extended,
            y=predictions_extended,
            mode='lines',
            name='Linha de Regressão',
            line=dict(color='red', width=2)
        ))
        
        # Predição específica
        fig_pred.add_trace(go.Scatter(
            x=[pred_year],
            y=[future_pred],
            mode='markers',
            name=f'Predição {pred_year}',
            marker=dict(color='orange', size=15, symbol='star')
        ))
        
        fig_pred.update_layout(
            title=title,
            xaxis_title='Ano',
            yaxis_title=y_label,
            hovermode='x unified'
        )
        
        # Gráfico de performance do modelo
        fig_perf = go.Figure()
        
        # Scatter plot: Real vs Predito
        fig_perf.add_trace(go.Scatter(
            x=y_test,
            y=y_pred_test,
            mode='markers',
            name='Teste',
            marker=dict(color='blue', size=8)
        ))
        
        fig_perf.add_trace(go.Scatter(
            x=y_train,
            y=y_pred_train,
            mode='markers',
            name='Treino',
            marker=dict(color='green', size=8)
        ))
        
        # Linha diagonal perfeita
        min_val = min(min(y_train), min(y_test))
        max_val = max(max(y_train), max(y_test))
        fig_perf.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Predição Perfeita',
            line=dict(color='red', dash='dash')
        ))
        
        fig_perf.update_layout(
            title='Performance do Modelo: Real vs Predito',
            xaxis_title='Valores Reais',
            yaxis_title='Valores Preditos'
        )
        
        return results, fig_pred, fig_perf
        
    except Exception as e:
        error_msg = html.Div([
            html.H4("❌ Erro na Análise", style={'color': 'red'}),
            html.P(f"Erro: {str(e)}")
        ])
        return error_msg, {}, {}

if __name__ == '__main__':
    app.run(debug=True)