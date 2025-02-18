import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html

# Dash App initialisieren
app = dash.Dash(__name__)
server = app.server  # Für Render Deployment

# Herz-Form mathematisch generieren
t = np.linspace(0, 2 * np.pi, 100)
x = 16 * np.sin(t) ** 3
y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)

# Animation erstellen
frames = [
    go.Frame(
        data=[
            go.Scatter(
                x=x[:i],
                y=y[:i],
                mode="lines",
                line=dict(color="red", width=3)
            )
        ]
    )
    for i in range(1, len(t) + 1)
]

fig = go.Figure(
    data=[
        go.Scatter(
            x=[],
            y=[],
            mode="lines",
            line=dict(color="red", width=3)
        )
    ],
    layout=go.Layout(
        title="💖 Bengisuuuuuuuuuuuuu Herz Animation",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False, scaleanchor="x"),
        showlegend=False,
        width=600,
        height=600,
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
