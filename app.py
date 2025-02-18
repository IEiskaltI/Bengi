import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html

# Dash App initialisieren
app = dash.Dash(__name__)
server = app.server  # Für Render Deployment

# Herz-Form mathematisch generieren
t = np.linspace(0, 2 * np.pi, 100)
x_herz = 16 * np.sin(t) ** 3
y_herz = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

# Koordinaten für "BENGISU" (optimiert für besser lesbare Buchstaben)
buchstaben_koordinaten = {
    "B": ([-6, -6, -6, -5, -4, -4, -5, -4, -4, -6], [4, -4, 0, 0, 1, 2, 2, 3, 4, 4]),
    "E": ([-3, -3, -3, -2, -2, -3, -3, -2], [4, -4, 4, 4, 0, 0, -4, -4]),
    "N": ([-1, -1, 0, 0], [4, -4, 4, -4]),
    "G": ([1, 1, 2, 3, 3, 2, 2], [4, -4, -4, -3, 1, 1, 2]),
    "I": ([4, 4], [4, -4]),
    "S": ([6, 7, 8, 7, 6, 7, 8], [4, 4, 3, 2, 1, 0, -1]),
    "U": ([10, 10, 11, 12, 12], [4, -3, -4, -3, 4])
}

# Zweites Herz unterhalb des ersten
x_herz2 = x_herz
y_herz2 = y_herz - 12  # Herz nach unten verschieben

# Frames für Animation erstellen
frames = []

# 1️⃣ Erstes Herz zeichnen
for i in range(1, len(t) + 1):
    frames.append(go.Frame(
        data=[go.Scatter(x=x_herz[:i], y=y_herz[:i], mode="lines", line=dict(color="red", width=3))]
    ))


# Plotly Figure
fig = go.Figure(
    data=[go.Scatter(x=[], y=[], mode="lines", line=dict(color="red", width=3))],
    layout=go.Layout(
        title="💖 Bengisu Animation 💖",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x"),
        showlegend=False,
        width=400,  # Kleinere Breite für Mobile
        height=600,  # Optimierte Höhe für Mobile
        margin=dict(l=10, r=10, t=50, b=10),  # Weniger Rand für mehr Platz auf Mobile
        updatemenus=[]
    ),
    frames=frames
)

# Dash Layout (optimiert für Mobile) mit "Start"-Button über dem Graphen
app.layout = html.Div([
    html.H1("Bengisuuuuuuuuuuuuu💗", style={
        'textAlign': 'center',
        'fontWeight': 'bold',
        'fontSize': '24px',
        'marginBottom': '10px'
    }),
    # html.Button("Start 💖", id="start-button", n_clicks=0, style={
    #     'display': 'block', 'margin': 'auto', 'padding': '10px 20px',
    #     'fontSize': '18px', 'backgroundColor': 'red', 'color': 'white', 'border': 'none',
    #     'borderRadius': '5px', 'cursor': 'pointer'
    # }),
    dcc.Graph(id="herz-animation", figure=fig, config={'responsive': True})
], style={'textAlign': 'center', 'maxWidth': '100%', 'overflowX': 'hidden'})

# Callback für Start-Button
@app.callback(
    dash.dependencies.Output("herz-animation", "figure"),
    [dash.dependencies.Input("start-button", "n_clicks")]
)
def start_animation(n_clicks):
    if n_clicks > 0:
        fig.update_layout(
            updatemenus=[dict(
                type="buttons",
                showactive=False,
                buttons=[dict(
                    label="Start 💖",
                    method="animate",
                    args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)]
                )]
            )]
        )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
