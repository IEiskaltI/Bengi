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

# Bengisu Buchstaben Koordinaten (angepasst für bessere Darstellung auf Mobile)
bengisu_x = np.array([-6, -6, -4, -4, np.nan,  # B
                      -3, -3, -3, np.nan,       # E
                      -2, -2, -2, np.nan,       # N
                      -1, -1, -1, np.nan,       # G
                       0,  0,  0, np.nan,       # I
                       1,  1,  1, np.nan,       # S
                       2,  2,  2])              # U

bengisu_y = np.array([3, -3, -3, 3, np.nan,    # B
                      3, -3, -3, np.nan,       # E
                      3, -3,  3, np.nan,       # N
                      3, -3, -2, np.nan,       # G
                      3, -3, -3, np.nan,       # I
                      3, -3, -2, np.nan,       # S
                      3, -3, -2])              # U

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

# ⏳ Leere Szene (Herz verschwindet, bevor "Bengisu" beginnt)
frames.append(go.Frame(data=[]))

# 2️⃣ "Bengisu" schreiben
for i in range(1, len(bengisu_x) + 1):
    frames.append(go.Frame(
        data=[
            go.Scatter(x=bengisu_x[:i], y=bengisu_y[:i], mode="lines", line=dict(color="blue", width=5))  # Buchstaben erscheinen
        ]
    ))

# 3️⃣ Zweites Herz zeichnen
for i in range(1, len(t) + 1):
    frames.append(go.Frame(
        data=[
            go.Scatter(x=bengisu_x, y=bengisu_y, mode="lines", line=dict(color="blue", width=5)),  # "Bengisu" bleibt
            go.Scatter(x=x_herz2[:i], y=y_herz2[:i], mode="lines", line=dict(color="red", width=3))  # Zweites Herz erscheint
        ]
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
        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="Start 💖",
                        method="animate",
                        args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)]
                    )
                ]
            )
        ]
    ),
    frames=frames
)

# Dash Layout (optimiert für Mobile)
app.layout = html.Div([
    html.H1("Bengisuuuuuuuuuuuuu💗", style={
        'textAlign': 'center',
        'fontWeight': 'bold',
        'fontSize': '24px',  # Kleinere Schrift für Mobile
        'marginBottom': '10px'
    }),
    dcc.Graph(id="herz-animation", figure=fig, config={'responsive': True})
], style={'textAlign': 'center', 'maxWidth': '100%', 'overflowX': 'hidden'})  # Responsives Design

if __name__ == '__main__':
    app.run_server(debug=True)
