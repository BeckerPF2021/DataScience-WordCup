import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from dash import html, no_update
import plotly.graph_objects as go

def make_ml_prediction(df_cups, df_matches, pred_year, pred_type):
    try:
        if pred_type == 'total_attendance':
            df_ml = df_cups[['Year', 'Attendance']].dropna().copy()
            scale = 1e6
            df_ml['Attendance'] /= scale
            target_col = 'Attendance'
            title = 'Público Total'
            y_label = 'Milhões'
            suffix = 'milhões'
        elif pred_type == 'avg_attendance':
            df_ml = df_matches.groupby('Year')['Attendance'].mean().reset_index().dropna().copy()
            scale = 1e3
            df_ml['Attendance'] /= scale
            target_col = 'Attendance'
            title = 'Público Médio'
            y_label = 'Milhares'
            suffix = 'milhares'
        else:
            df_ml = df_cups[['Year', 'GoalsScored']].dropna().copy()
            scale = 1
            target_col = 'GoalsScored'
            title = 'Gols Marcados'
            y_label = 'Gols'
            suffix = 'gols'

        if len(df_ml) < 3:
            return html.P("Dados insuficientes para análise."), no_update, no_update

        X = df_ml[['Year']].values
        y = df_ml[target_col].values

        if len(df_ml) >= 6:
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        else:
            X_train, X_test, y_train, y_test = X, X, y, y

        model = LinearRegression().fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_test = model.predict(X_test)

        r2_val = r2_score(y_test, y_pred_test) if len(df_ml) >= 6 else r2_score(y_train, y_pred_train)
        rmse_val = np.sqrt(mean_squared_error(y_test, y_pred_test))

        future_pred = abs(model.predict([[pred_year]])[0])

        # Valor real da última Copa disponível no dataset
        last_year = df_ml['Year'].max()
        last_real = df_ml[df_ml['Year'] == last_year][target_col].values[0]

        pred_fmt = f"{future_pred:,.1f} {suffix}"
        real_fmt = f"{last_real:,.1f} {suffix}"

        results = html.Div([
            html.H3(f"🔮 Predição {pred_year}: {pred_fmt}"),
            html.P(f"📊 Última Copa ({last_year}): {real_fmt}"),
            html.P(f"R² = {r2_val:.2f}, RMSE = {rmse_val:.2f} {suffix}")
        ])

        years_ext = np.arange(df_ml['Year'].min(), pred_year + 1)
        preds_ext = model.predict(years_ext.reshape(-1, 1))

        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(x=df_ml['Year'], y=df_ml[target_col], mode='markers', name='Histórico'))
        fig_pred.add_trace(go.Scatter(x=years_ext, y=preds_ext, mode='lines', name='Regressão'))
        fig_pred.add_trace(go.Scatter(x=[pred_year], y=[future_pred], mode='markers', name='Predição', marker=dict(size=12)))
        fig_pred.add_trace(go.Scatter(x=[last_year], y=[last_real], mode='markers+text',
                                      name=f'Real {last_year}', marker=dict(color='green', size=10),
                                      text=[f"Real {last_year}"], textposition='top center'))
        fig_pred.update_layout(title=title, xaxis_title='Ano', yaxis_title=y_label)

        fig_perf = go.Figure()
        fig_perf.add_trace(go.Scatter(x=y_test, y=y_pred_test, mode='markers', name='Teste'))
        fig_perf.add_trace(go.Scatter(x=y_train, y=y_pred_train, mode='markers', name='Treino'))
        lim = [min(min(y_train), min(y_test)), max(max(y_train), max(y_test))]
        fig_perf.add_trace(go.Scatter(x=lim, y=lim, mode='lines', name='Perfeita', line=dict(dash='dash')))
        fig_perf.update_layout(title='Performance do Modelo', xaxis_title='Real', yaxis_title='Previsto')

        return results, fig_pred, fig_perf

    except Exception as e:
        return html.Div([html.H4("❌ Erro na Análise"), html.P(str(e))]), no_update, no_update