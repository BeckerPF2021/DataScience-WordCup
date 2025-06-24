import os
from dash import Dash
from data_loader import load_and_prepare_data
from stats import save_descriptive_stats
from layouts import (
    get_cups_layout, get_matches_layout, get_players_layout,
    get_relacao_layout, get_ml_layout, get_main_layout
)
from callbacks import register_callbacks

# Criar pastas se não existirem
os.makedirs('output', exist_ok=True)
os.makedirs('plots', exist_ok=True)

# Carregar dados
df_cups, df_matches, df_players = load_and_prepare_data()

# Salvar estatísticas
save_descriptive_stats(df_cups, df_matches, df_players)

# Preparar layouts
layouts = {
    'cups': get_cups_layout(df_cups),
    'matches': get_matches_layout(df_matches),
    'players': get_players_layout(df_players),
    'relacao': get_relacao_layout(df_cups),
    'ml': get_ml_layout()
}

# Inicializar app
app = Dash(__name__)
app.title = "🏆 FIFA - Copas do Mundo"
app.config.suppress_callback_exceptions = True

# Layout principal
app.layout = get_main_layout()

# Registrar callbacks
register_callbacks(app, df_cups, df_matches, df_players, layouts)

if __name__ == '__main__':
    app.run(debug=True)