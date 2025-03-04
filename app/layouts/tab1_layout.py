from dash import html, dcc
import dash_bootstrap_components as dbc


def get_tab1_layout():
    """Layout for Tab 1: Season Performance Overview."""
    return dbc.Container(
        [
            # Dashboard Header
            html.H3("Season Performance Dashboard", className="mt-4"),
            html.P(
                "Track your fantasy team's performance across the season and analyze the impact of roster moves and lineup decisions.",
                className="text-muted",
            ),
            # Control Panel
            dbc.Card(
                [
                    dbc.CardHeader("Dashboard Controls"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            dbc.Label("Select Team:"),
                                            dcc.Dropdown(
                                                id="team-dropdown",
                                                options=[
                                                    {"label": f"Team {i}", "value": i}
                                                    for i in range(1, 11)
                                                ],
                                                value=1,
                                                clearable=False,
                                            ),
                                        ],
                                        md=6,
                                    ),
                                    dbc.Col(
                                        [
                                            dbc.Label("Select View:"),
                                            dbc.RadioItems(
                                                id="view-toggle",
                                                options=[
                                                    {
                                                        "label": "Show All",
                                                        "value": "all",
                                                    },
                                                    {
                                                        "label": "Roster Comparison",
                                                        "value": "roster_comparison",
                                                    },
                                                    {
                                                        "label": "Lineup Decisions",
                                                        "value": "lineup_comparison",
                                                    },
                                                ],
                                                value="all",
                                                inline=True,
                                            ),
                                        ],
                                        md=6,
                                    ),
                                ]
                            ),
                            html.Div(
                                [
                                    html.I(className="fas fa-info-circle me-2"),
                                    html.Span(
                                        "Hover over data points for details. Click on a week to see detailed analysis."
                                    ),
                                ],
                                className="text-muted fst-italic mt-3 small",
                            ),
                        ]
                    ),
                ],
                className="mb-4 shadow-sm",
            ),
            # Summary Cards Section
            html.Div(
                [
                    html.H4("Season Performance Summary", className="mb-3"),
                    dcc.Loading(
                        id="loading-summary-cards",
                        type="circle",
                        children=html.Div(id="season-summary-cards"),
                    ),
                ],
                className="mb-4",
            ),
            # Season Overview Chart
            dbc.Card(
                [
                    dbc.CardHeader("Weekly Performance Trend"),
                    dbc.CardBody(
                        [
                            dcc.Loading(
                                id="loading-chart",
                                type="circle",
                                children=dcc.Graph(
                                    id="season-overview-chart",
                                    config={"displayModeBar": False},
                                    figure={
                                        "layout": {
                                            "legend": {
                                                "orientation": "h",
                                                "y": -0.2,
                                                "x": 0.5,
                                                "xanchor": "center",
                                            }
                                        }
                                    },
                                ),
                            ),
                        ]
                    ),
                ],
                className="mb-4 shadow-sm",
            ),
            # Waterfall Analysis
            dbc.Card(
                [
                    dbc.CardHeader("Season Performance Breakdown"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        [
                                            html.P(
                                                "This chart shows how draft value, transactions, and lineup decisions contributed to your final score.",
                                                className="text-muted mb-3",
                                            ),
                                            dcc.Loading(
                                                id="loading-waterfall",
                                                type="circle",
                                                children=dcc.Graph(
                                                    id="season-waterfall"
                                                ),
                                            ),
                                        ],
                                        width={"size": 10, "offset": 1},
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
                className="mb-4 shadow-sm",
            ),
        ],
        fluid=True,
    )
