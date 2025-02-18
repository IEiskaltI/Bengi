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

# Bengisu Buchstaben Koordinaten (grob vereinfacht)
bengisu_x = np.array([-8, -8, -6, -6, np.nan,  # B
                      -4, -4, -4, np.nan,       # E
                      -2, -2, -2, np.nan,       # N
                       0,  0,  0, np.nan,       # G
                       2,  2,  2, np.nan,       # I
                       4,  4,  4, np.nan,       # S
                       6,  6,  6])              # U

bengisu_y = np.array([4, -4, -4, 4, np.nan,    # B
                      4, -4, -4, np.nan,       # E
                      4, -4,  4, np.nan,       # N
                      4, -4, -2, np.nan,       # G
                      4, -4, -4, np.nan,       # I
                      4, -4, -2, np.nan,       # S
                      4, -4, -2])              # U

# Zweites Herz unterhalb des ersten
x_herz2 = x_herz
y_herz2 = y_herz - 15  # nach unten verschieben

# Frames für Animation erstellen
frames = []

# Erstes Herz zeichnen
for i in range(1, len(t) + 1):
    frames.append(go.Frame(
        data=[go.Scatter(x=x_herz[:i], y=y_herz[:i], mode="lines", line=dict(color="red", width=3))]
    ))

# "Bengisu" schreiben
for i in range(1, len(bengisu_x) + 1):
    frames.append(go.Frame(
        data=[
            go.Scatter(x=x_herz, y=y_herz, mode="lines", line=dict(color="red", width=3)),  # Erstes Herz bleibt
            go.Scatter(x=bengisu_x[:i], y=bengisu_y[:i], mode="lines", line=dict(color="blue", width=5))  # Buchstaben erscheinen
        ]
    ))

# Zweites Herz zeichnen
for i in range(1, len(t) + 1):
    frames.append(go.Frame(
        data=[
            go.Scatter(x=x_herz, y=y_herz, mode="lines", line=dict(color="red", width=3)),  # Erstes Herz bleibt
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
        width=600,
        height=800,
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

# Dash Layout
app.layout = html.Div([
    html.H1("Bengisuuuuuuuuuuuuu💗", style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': '32px'}),
    dcc.Graph(id="herz-animation", figure=fig)
])

if __name__ == '__main__':
    app.run_server(debug=True)
