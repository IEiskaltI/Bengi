import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Anzahl der Simulationen
num_simulationen = 1000

# Zufällige Werte für die Eingangsparameter im angegebenen Bereich
np.random.seed(42)
monatliche_rate = np.random.uniform(2000, 3000, num_simulationen)
zinsen_prozent = np.random.uniform(2.3, 3.5, num_simulationen)
eigenkapital = np.random.uniform(10000, 40000, num_simulationen)
hauspreis = np.random.uniform(300000, 1000000, num_simulationen)

# Berechnung der Laufzeit für jede Simulation
laufzeiten = []

for i in range(num_simulationen):
    darlehenssumme = hauspreis[i] - eigenkapital[i]
    restschuld = darlehenssumme
    zinssatz = zinsen_prozent[i] / 100
    jahres_rate = monatliche_rate[i] * 12
    jahr = 0
    
    while restschuld > 0:
        jahr += 1
        zinsen_euro = restschuld * zinssatz
        
        if restschuld + zinsen_euro <= jahres_rate:
            tilgung_euro = restschuld
            restschuld = 0
        else:
            tilgung_euro = jahres_rate - zinsen_euro
            restschuld -= tilgung_euro
        
        if tilgung_euro < 0:
            jahr = np.nan  # Nicht tilgbar
            break
    
    laufzeiten.append(jahr)

# Funktion zum Filtern der Daten basierend auf der maximalen Laufzeit
def filter_data(max_laufzeit):
    filtered_indices = [i for i in range(num_simulationen) if laufzeiten[i] <= max_laufzeit]
    return (
        monatliche_rate[filtered_indices],
        zinsen_prozent[filtered_indices],
        hauspreis[filtered_indices] - eigenkapital[filtered_indices],
        [laufzeiten[i] for i in filtered_indices]
    )

# Dash App initialisieren
app = dash.Dash(__name__)
server = app.server  # Für Render Deployment

app.layout = html.Div([
    html.H1("Bengisuuuuuuuuuuuuu💗", style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '32px'}),
    dcc.Slider(
        id='laufzeit-slider',
        min=1,
        max=int(np.nanmax(laufzeiten)),
        step=1,
        value=int(np.nanmax(laufzeiten)),
        marks={i: str(i) for i in range(1, int(np.nanmax(laufzeiten))+1, 5)},
    ),
    dcc.Graph(id='scatter-plot')
])

@app.callback(
    Output('scatter-plot', 'figure'),
    Input('laufzeit-slider', 'value')
)
def update_figure(max_laufzeit):
    x, y, z, colors = filter_data(max_laufzeit)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',
        marker=dict(
            size=5,
            color=colors,
            colorscale='Plasma',
            colorbar=dict(title='Laufzeit (Jahre)')
        ),
        hovertemplate=(
            "Monatliche Rate: %{x:.2f} €<br>"
            "Zinssatz: %{y:.2f} %<br>"
            "Hauspreis - Eigenkapital: %{z:.2f} €<br>"
            "Laufzeit: %{marker.color:.0f} Jahre"
        )
    ))
    
    fig.update_layout(
        scene=dict(
            xaxis_title='Monatliche Rate (Euro)',
            yaxis_title='Zinssatz (%)',
            zaxis_title='Hauspreis - Eigenkapital (Euro)',
            xaxis=dict(range=[2000, 3000]),
            yaxis=dict(range=[2.3, 3.5]),
            zaxis=dict(range=[min(hauspreis - eigenkapital), max(hauspreis - eigenkapital)])
        ),
        title='Monte Carlo Simulation: Laufzeit der Kreditrückzahlung',
        width=1200,
        height=800
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
