from dash import html, dcc
import dash_bootstrap_components as dbc


def get_tab1_layout():
    """Layout for Tab 1: Season Performance Overview."""
    return dbc.Container(
        [
            # Dashboard Header with Team Selector
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3("Season Performance Dashboard", className="mt-4"),
                            html.P(
                                "Track your fantasy team's performance across the season and analyze the impact of roster moves and lineup decisions.",
                                className="text-muted",
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div(
                                            [
                                                dbc.Label(
                                                    "Select Team:", className="mb-1"
                                                ),
                                                dcc.Dropdown(
                                                    id="team-dropdown",
                                                    options=[
                                                        {
                                                            "label": f"Team {i}",
                                                            "value": i,
                                                        }
                                                        for i in range(1, 11)
                                                    ],
                                                    value=1,
                                                    clearable=False,
                                                ),
                                            ],
                                            className="mb-4",  # Add margin-top for spacing
                                        ),
                                        width=3,  # Adjust the width of the dropdown
                                    ),
                                ],
                                className="mt-3",  # Add margin-top for spacing
                            ),
                        ],
                        md=12,
                    ),
                ],
                className="mb-3 align-items-center",
            ),
            # Summary Cards Section
            html.Div(
                [
                    html.H4("Season Performance Summary", className="mb-3"),
                    html.P(
                        "See how your draft, transactions, and lineup decisions affected your final score",
                        className="text-muted mb-3",
                    ),
                    # Two-column layout for summary cards and waterfall chart
                    dbc.Row(
                        [
                            # Left column: Summary Cards
                            dbc.Col(
                                html.Div(  # Outer container for centering
                                    [
                                        html.Div(
                                            dbc.Button(
                                                [
                                                    html.I(
                                                        className="fas fa-info-circle me-1"
                                                    ),
                                                    "How to read this",
                                                ],
                                                id="summary-explainer-button",
                                                color="link",
                                                size="sm",
                                                # className="",  # Add margin-top for spacing
                                            ),
                                            className="d-flex justify-content-start w-100",  # Left justify the button
                                        ),
                                        dcc.Loading(
                                            id="loading-summary-cards",
                                            type="circle",
                                            children=html.Div(
                                                id="season-summary-cards",
                                            ),
                                        ),
                                    ],
                                    className="d-flex flex-column align-items-center justify-content-center h-100",  # Apply centering here
                                    style={"height": "100%"},
                                ),
                                md=6,
                                className="mb-3",
                            ),
                            # Right column: Waterfall Chart
                            dbc.Col(
                                dbc.Card(
                                    [
                                        dbc.CardHeader("Season Performance Breakdown"),
                                        dbc.CardBody(
                                            dcc.Loading(
                                                id="loading-waterfall",
                                                type="circle",
                                                children=dcc.Graph(
                                                    id="season-waterfall",
                                                    style={"height": "410px"},
                                                    config={
                                                        "responsive": True,
                                                        # "displayModeBar": False,
                                                    },
                                                ),
                                            ),
                                        ),
                                    ],
                                    className="h-100 shadow-sm",  # Make card fill height
                                ),
                                md=6,
                                className="mb-3",
                            ),
                        ],
                        className="mb-4 align-items-stretch",
                        style={
                            "minHeight": "450px"
                        },  # Set a minimum height for the row
                    ),
                ],
                className="mb-4",
            ),
            # Weekly Performance Trend (full width)
            html.Div(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H4("Weekly Summary", className="mb-0"),
                                    html.P(
                                        "Analyze the weekly impact of your roster moves and lineup decisions",
                                        className="text-muted",
                                    ),
                                    html.Div(
                                        [
                                            html.Div(
                                                html.H6("View Mode", className="mt-4"),
                                            ),
                                            dbc.Card(
                                                dbc.CardBody(
                                                    [
                                                        dbc.RadioItems(
                                                            id="view-toggle",
                                                            options=[
                                                                {
                                                                    "label": [
                                                                        html.Span(
                                                                            "Roster Comparison ",
                                                                            className="fw-bold",
                                                                        ),
                                                                        html.Span(
                                                                            "- View weekly impact of transactions",
                                                                            className="text-muted small",
                                                                        ),
                                                                    ],
                                                                    "value": "roster_comparison",
                                                                },
                                                                {
                                                                    "label": [
                                                                        html.Span(
                                                                            "Lineup Decisions ",
                                                                            className="fw-bold",
                                                                        ),
                                                                        html.Span(
                                                                            "- Analyze weekly start/sit decision quality",
                                                                            className="text-muted small",
                                                                        ),
                                                                    ],
                                                                    "value": "lineup_comparison",
                                                                },
                                                            ],
                                                            value="roster_comparison",
                                                            inline=False,
                                                            className="my-1",
                                                        ),
                                                    ]
                                                ),
                                                className="border-light bg-light mb-3",
                                                style={"maxWidth": "465px"},
                                            ),
                                            html.Div(
                                                [
                                                    html.I(
                                                        className="fas fa-info-circle me-2"
                                                    ),
                                                    html.Span(
                                                        "Hover over data points for details. Click on a week to see detailed analysis."
                                                    ),
                                                ],
                                                className="text-muted fst-italic small text-start mt-1",
                                            ),
                                        ],
                                        className="mt-3",
                                    ),
                                ],
                                md=12,
                            ),
                        ],
                        className="mb-1 align-items-center",
                    ),
                    dbc.Card(
                        [
                            dbc.CardHeader("Weekly Performance Trend"),
                            dbc.CardBody(
                                dcc.Loading(
                                    id="loading-chart",
                                    type="circle",
                                    children=dcc.Graph(
                                        id="season-overview-chart",
                                        style={"height": "450px"},
                                        config={"displayModeBar": False},
                                    ),
                                )
                            ),
                        ],
                        className="mb-4 shadow-sm",
                    ),
                    # Add this at the bottom before the final return statement's closing parenthesis
                    # Educational Modal for explaining concepts
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Understanding Your Fantasy Performance"),
                            dbc.ModalBody(
                                [
                                    html.H5(
                                        "We analyze your season in three key components:",
                                        className="mb-3",
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    html.Div(
                                                        [
                                                            html.I(
                                                                className="fas fa-drafting-compass fa-2x text-primary"
                                                            ),
                                                            html.H5(
                                                                "Draft Baseline",
                                                                className="text-primary mt-2",
                                                            ),
                                                            html.P(
                                                                "This is your foundation - how many points your originally drafted team would score with perfect lineup decisions but no roster changes."
                                                            ),
                                                            html.P(
                                                                "It represents the quality of your draft strategy.",
                                                                className="small text-muted",
                                                            ),
                                                        ],
                                                        className="text-center p-3 border rounded h-100",
                                                    )
                                                ],
                                                width=4,
                                            ),
                                            dbc.Col(
                                                [
                                                    html.Div(
                                                        [
                                                            html.I(
                                                                className="fas fa-exchange-alt fa-2x text-success"
                                                            ),
                                                            html.H5(
                                                                "Transaction Impact",
                                                                className="text-success mt-2",
                                                            ),
                                                            html.P(
                                                                "This shows how your add/drops and trades throughout the season affected your team's potential."
                                                            ),
                                                            html.P(
                                                                "Positive numbers mean your roster improved; negative means it got worse.",
                                                                className="small text-muted",
                                                            ),
                                                        ],
                                                        className="text-center p-3 border rounded h-100",
                                                    )
                                                ],
                                                width=4,
                                            ),
                                            dbc.Col(
                                                [
                                                    html.Div(
                                                        [
                                                            html.I(
                                                                className="fas fa-chess fa-2x text-warning"
                                                            ),
                                                            html.H5(
                                                                "Lineup Efficiency",
                                                                className="text-warning mt-2",
                                                            ),
                                                            html.P(
                                                                "This measures how well you selected your starting lineup each week from available players."
                                                            ),
                                                            html.P(
                                                                "100% means you made perfect lineup decisions every week.",
                                                                className="small text-muted",
                                                            ),
                                                        ],
                                                        className="text-center p-3 border rounded h-100",
                                                    )
                                                ],
                                                width=4,
                                            ),
                                        ],
                                        className="mb-4",
                                    ),
                                    html.Hr(),
                                    html.P(
                                        [
                                            "Combined, these three factors determine your final season performance. ",
                                            "Use the charts to see how each factor contributed to your weekly scores.",
                                        ],
                                        className="mt-3",
                                    ),
                                ]
                            ),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Got it!",
                                    id="summary-explainer-close",
                                    className="ms-auto",
                                )
                            ),
                        ],
                        id="summary-explainer-modal",
                        size="lg",
                    ),
                ],
            ),
        ],
        fluid=True,
    )
