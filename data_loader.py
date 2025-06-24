import pandas as pd

def load_and_prepare_data():
    # Dados de Copas do Mundo
    df_cups = pd.read_csv("data/WorldCups.csv")
    df_cups.columns = df_cups.columns.str.strip()
    expected_cups = ['Year', 'Country', 'Winner', 'Runners-Up', 'GoalsScored', 'Attendance', 'QualifiedTeams']
    assert all(col in df_cups.columns for col in expected_cups), "Colunas faltando em WorldCups.csv"
    df_cups = df_cups.dropna(subset=['Year', 'Country']).copy()
    df_cups['Year'] = pd.to_numeric(df_cups['Year'], errors='coerce')
    df_cups['GoalsScored'] = pd.to_numeric(df_cups['GoalsScored'], errors='coerce')
    df_cups['Attendance'] = pd.to_numeric(df_cups['Attendance'], errors='coerce')
    df_cups['QualifiedTeams'] = pd.to_numeric(df_cups['QualifiedTeams'], errors='coerce')

    # Dados de Partidas
    df_matches = pd.read_csv("data/WorldCupMatches.csv")
    df_matches.columns = df_matches.columns.str.strip()
    expected_matches = ['Year', 'Stage', 'Home Team Goals', 'Away Team Goals', 'Attendance']
    assert all(col in df_matches.columns for col in expected_matches), "Colunas faltando em WorldCupMatches.csv"
    df_matches = df_matches.dropna(subset=['Stage']).copy()
    df_matches['Home Team Goals'] = pd.to_numeric(df_matches['Home Team Goals'], errors='coerce')
    df_matches['Away Team Goals'] = pd.to_numeric(df_matches['Away Team Goals'], errors='coerce')
    df_matches['Attendance'] = pd.to_numeric(df_matches['Attendance'], errors='coerce')

    # Dados de Jogadores
    df_players = pd.read_csv("data/WorldCupPlayers.csv")
    df_players.columns = df_players.columns.str.strip()

    expected_players = ['Player Name', 'Position', 'Shirt Number', 'Event', 'Team Initials']
    assert all(col in df_players.columns for col in expected_players), "Colunas faltando em WorldCupPlayers.csv"

    df_players = df_players.dropna(subset=['Player Name', 'Team Initials', 'Event']).copy()
    df_players['Shirt Number'] = pd.to_numeric(df_players['Shirt Number'], errors='coerce')

    # Filtra apenas eventos que contenham pelo menos um gol (G seguido de minuto)
    df_players = df_players[df_players['Event'].str.contains(r"G\d+", na=False)]

    return df_cups, df_matches, df_players

