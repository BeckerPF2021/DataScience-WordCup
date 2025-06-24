import pandas as pd

def save_descriptive_stats(df_cups, df_matches, df_players):
    # Estatísticas descritivas padrão
    stats_cups = df_cups.describe(include='all').transpose()
    stats_cups['dataset'] = 'WorldCups'

    stats_matches = df_matches.describe(include='all').transpose()
    stats_matches['dataset'] = 'WorldCupMatches'

    stats_players = df_players.describe(include='all').transpose()
    stats_players['dataset'] = 'WorldCupPlayers'

    # Estatísticas customizadas
    custom_stats = []

    # 1. Total de gols por edição (WorldCupMatches)
    df_matches['TotalGoals'] = df_matches['Home Team Goals'] + df_matches['Away Team Goals']
    total_goals = df_matches.groupby('Year')['TotalGoals'].sum().reset_index(name='Total Goals')
    total_goals['Stat'] = 'Total de Gols por Edição'
    total_goals['dataset'] = 'WorldCupMatches'
    custom_stats.append(total_goals)

    # 2. Média de público por partida (WorldCupMatches)
    avg_attendance = df_matches.groupby('Year')['Attendance'].mean().reset_index(name='Média de Público por Jogo')
    avg_attendance['Stat'] = 'Média Público por Partida'
    avg_attendance['dataset'] = 'WorldCupMatches'
    custom_stats.append(avg_attendance)

    # 3. Quantidade de jogadores únicos por Copa (usando MatchID como base)
    unique_players = df_players.groupby('MatchID')['Player Name'].nunique().reset_index(name='Jogadores por Partida')
    total_players = df_matches[['Year', 'MatchID']].merge(unique_players, on='MatchID')
    players_per_year = total_players.groupby('Year')['Jogadores por Partida'].sum().reset_index(name='Total de Jogadores')
    players_per_year['Stat'] = 'Total de Jogadores por Edição'
    players_per_year['dataset'] = 'WorldCupPlayers'
    custom_stats.append(players_per_year)

    # Junta tudo
    stats_basicos = pd.concat([stats_cups, stats_matches, stats_players])
    estatisticas_personalizadas = pd.concat(custom_stats, ignore_index=True)

    # Exporta
    final_stats = pd.concat([stats_basicos, estatisticas_personalizadas], sort=False)
    final_stats.to_csv('output/descriptive_stats.csv', index=False)
