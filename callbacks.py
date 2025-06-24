from dash import Input, Output, no_update, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from ml_model import make_ml_prediction
from plots import save_figure

def empty_fig(title="Sem dados para exibir"):
    fig = go.Figure()
    fig.add_annotation(
        dict(text=title,
             xref="paper", yref="paper",
             showarrow=False,
             font=dict(size=20, color="gray"))
    )
    fig.update_layout(
        xaxis={"visible": False},
        yaxis={"visible": False},
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    return fig

def preprocess_df_cups(df_cups):
    # Ajustar Attendance: remover pontos e converter para numérico
    if df_cups['Attendance'].dtype == object:
        df_cups['Attendance'] = df_cups['Attendance'].str.replace('.', '', regex=False)
    df_cups['Attendance'] = pd.to_numeric(df_cups['Attendance'], errors='coerce')

    # Converter outras colunas importantes
    df_cups['GoalsScored'] = pd.to_numeric(df_cups['GoalsScored'], errors='coerce')
    df_cups['QualifiedTeams'] = pd.to_numeric(df_cups['QualifiedTeams'], errors='coerce')
    df_cups['MatchesPlayed'] = pd.to_numeric(df_cups['MatchesPlayed'], errors='coerce')
    df_cups['Year'] = pd.to_numeric(df_cups['Year'], errors='coerce')

    return df_cups

def register_callbacks(app, df_cups, df_matches, df_players, layouts):

    df_cups = preprocess_df_cups(df_cups)

    cups_layout = layouts['cups']
    matches_layout = layouts['matches']
    players_layout = layouts['players']
    relacao_layout = layouts['relacao']
    ml_layout = layouts['ml']

    @app.callback(
        Output('page-content', 'children'),
        Input('btn-cups','n_clicks'),
        Input('btn-matches','n_clicks'),
        Input('btn-players','n_clicks'),
        Input('btn-relacao','n_clicks'),
        Input('btn-ml','n_clicks')
    )
    def display_page(n1, n2, n3, n4, n5):
        if not any([n1, n2, n3, n4, n5]):
            return cups_layout
        mx = max(n1, n2, n3, n4, n5)
        if mx == n5:
            return ml_layout
        if mx == n4:
            return relacao_layout
        if mx == n3:
            return players_layout
        if mx == n2:
            return matches_layout
        return cups_layout

    @app.callback(Output('graph-goals','figure'), Input('dropdown-host','value'))
    def update_goals(selected):
        df = df_cups[df_cups['Country'] == selected] if selected else df_cups
        if df.empty:
            return empty_fig("Nenhuma Copa encontrada para esse país-sede.")
        fig = px.bar(
            df, x='Year', y='GoalsScored', color='Country',
            title='Gols por Copa do Mundo',
            labels={'Year':'Ano', 'GoalsScored':'Gols Marcados', 'Country':'País-Sede'},
            hover_data=['Winner','Runners-Up','QualifiedTeams']
        )
        fig.update_layout(transition_duration=500)
        save_figure(fig, 'goals_cups.png')
        return fig

    @app.callback(Output('graph-attendance','figure'), Input('dropdown-host','value'))
    def update_attendance(selected):
        df = df_cups[df_cups['Country'] == selected] if selected else df_cups
        if df.empty or df['Attendance'].isna().all():
            return empty_fig("Nenhum dado de público para esse país-sede.")
        fig = px.line(
            df, x='Year', y='Attendance',
            title='Público por Copa do Mundo',
            labels={'Year':'Ano', 'Attendance':'Público'},
            markers=True
        )
        fig.update_layout(transition_duration=500)
        save_figure(fig, 'attendance_cups.png')
        return fig

    @app.callback(Output('graph-titles','figure'), Input('dropdown-host','value'))
    def update_titles(selected):
        df = df_cups[df_cups['Country'] == selected] if selected else df_cups
        if df.empty:
            return empty_fig("Nenhum título encontrado para esse país-sede.")
        titles = df['Winner'].value_counts().reset_index()
        titles.columns = ['País','Títulos']
        if titles.empty:
            return empty_fig("Nenhum título disponível.")
        fig = px.pie(
            titles, values='Títulos', names='País', hole=0.4,
            title='Distribuição de Títulos por País',
            labels={'Títulos':'Número de Títulos','País':'País'}
        )
        fig.update_layout(transition_duration=500)
        save_figure(fig, 'titles_pie.png')
        return fig

    @app.callback(Output('graph-match-goals','figure'), Input('dropdown-stage','value'))
    def update_match_goals(stage):
        dfm = df_matches[df_matches['Stage'] == stage].copy() if stage else df_matches.copy()
        if dfm.empty:
            return empty_fig("Nenhuma partida encontrada para essa fase.")
        dfm['Total Goals'] = dfm['Home Team Goals'] + dfm['Away Team Goals']
        fig = px.histogram(
            dfm, x='Total Goals', nbins=15,
            title='Distribuição de Gols por Partida',
            labels={'Total Goals':'Gols Totais'}
        )
        fig.update_layout(transition_duration=500)
        save_figure(fig, 'match_goals_histogram.png')
        return fig

    @app.callback(Output('graph-attendance-matches','figure'), Input('dropdown-stage','value'))
    def update_match_attendance(stage):
        dfm = df_matches[df_matches['Stage'] == stage] if stage else df_matches
        if dfm.empty or dfm['Attendance'].isna().all():
            return empty_fig("Nenhum dado de público para essa fase.")
        fig = px.box(
            dfm, y='Attendance', points='all',
            title='Distribuição de Público por Fase',
            labels={'Attendance':'Público'}
        )
        fig.update_layout(transition_duration=500)
        save_figure(fig, 'match_attendance_box.png')
        return fig

    @app.callback(
        Output('players-list','children'),
        Output('graph-events','figure'),
        Input('dropdown-team','value')
    )
    def update_players_and_events(team):
        dfp = df_players[df_players['Team Initials'] == team] if team else df_players
        if dfp.empty:
            table = html.P("Nenhum jogador encontrado para este time.")
            fig = empty_fig("Nenhum evento disponível.")
            return table, fig

        table = html.Table(
            [html.Tr([html.Th(x) for x in ['Nome','Posição','Camisa','Evento']])] +
            [html.Tr([html.Td(r['Player Name']), html.Td(r['Position']), html.Th(r['Shirt Number']), html.Td(r['Event'])]) for _, r in dfp.iterrows()]
        )
        counts = dfp.groupby('Position')['Event'].count().reset_index()
        fig = px.bar(
            counts, x='Position', y='Event',
            title='Eventos por Posição',
            labels={'Position':'Posição','Event':'Quantidade de Eventos'}
        )
        fig.update_layout(transition_duration=500)
        save_figure(fig, 'player_events_by_position.png')
        return table, fig

    @app.callback(Output('graph-edition-matches','figure'), Input('dropdown-year','value'))
    def update_edition_matches(year):
        dfm = df_matches[df_matches['Year'] == year] if year else df_matches
        if dfm.empty:
            return empty_fig("Nenhuma partida encontrada para essa edição.")
        total = len(dfm)
        avg_g = (dfm['Home Team Goals'] + dfm['Away Team Goals']).mean()
        avg_a = dfm['Attendance'].mean()
        df_stats = pd.DataFrame({
            'Métrica':['Total de Partidas','Média de Gols/Jogo','Média de Público/Jogo'],
            'Valor':[total, avg_g, avg_a]
        })
        fig = px.bar(
            df_stats, x='Métrica', y='Valor',
            title='Estatísticas de Partidas por Edição',
            labels={'Métrica':'Métrica','Valor':'Valor'}
        )
        return fig

    @app.callback(Output('graph-edition-cups','figure'), Input('dropdown-year','value'))
    def update_edition_cups(year):
        dfc = df_cups[df_cups['Year'] == year] if year else df_cups
        if dfc.empty:
            return empty_fig("Nenhuma edição encontrada.")
        g = dfc['GoalsScored'].iloc[0]
        a = dfc['Attendance'].iloc[0]
        t = dfc['QualifiedTeams'].iloc[0]
        dfc_stats = pd.DataFrame({
            'Métrica':['Gols na Edição','Público na Edição','Times Qualificados'],
            'Valor':[g, a, t]
        })
        fig = px.bar(
            dfc_stats, x='Métrica', y='Valor',
            title='Estatísticas da Edição',
            labels={'Métrica':'Métrica','Valor':'Valor'}
        )
        return fig

    @app.callback(Output('graph-goals-correlation','figure'), Input('dropdown-year','value'))
    def update_goals_correlation(year):
        dfa = df_matches.copy()
        dfa['TotalGoals'] = dfa['Home Team Goals'] + dfa['Away Team Goals']
        summary = (
            dfa.groupby('Year')
               .agg(avg_goals=('TotalGoals','mean'), matches=('TotalGoals','size'))
               .reset_index()
               .merge(df_cups[['Year','GoalsScored','QualifiedTeams']], on='Year')
        )
        if year:
            summary = summary[summary['Year'] == year]
        if summary.empty:
            return empty_fig("Nenhuma correlação encontrada para esse ano.")
        fig = px.scatter(
            summary, x='GoalsScored', y='avg_goals', size='matches',
            hover_name=summary['Year'].astype(int),
            title='Correlação: Gols na Edição × Média de Gols por Partida',
            labels={
                'GoalsScored':'Gols na Edição',
                'avg_goals':'Média de Gols/Jogo',
                'matches':'Número de Partidas'
            }
        )
        return fig

    @app.callback(
        Output('ml-results', 'children'),
        Output('ml-prediction-graph', 'figure'),
        Output('ml-model-performance', 'figure'),
        Input('prediction-year', 'value'),
        Input('prediction-type', 'value')
    )
    def update_ml_predictions(pred_year, pred_type):
        return make_ml_prediction(df_cups, df_matches, pred_year, pred_type)
