import dash_bootstrap_components as dbc
from dash import html

from app.app import app
from app.layouts.tab1_layout import get_tab1_layout
from app.layouts.tab2_layout import get_tab2_layout
from app.layouts.tab3_layout import get_tab3_layout

# App layout
app.layout = dbc.Container(
    [
        html.H1("Fantasy Football Wrapped", className="my-4 text-center"),
        html.P(
            "(Current POC uses data from my own 2024 ESPN fantasy football team)",
            className="my-4 text-center",
        ),
        dbc.Tabs(
            [
                dbc.Tab(get_tab1_layout(), label="Season Overview"),
                dbc.Tab(get_tab2_layout(), label="Weekly Analysis"),
                dbc.Tab(get_tab3_layout(), label="League Breakdown"),
            ]
        ),
        # Footer with credits
        html.Footer(
            [
                html.Hr(),
                html.P(
                    "Fantasy Football Wrapped - 2024",
                    className="text-center text-muted",
                ),
            ],
            className="mt-5",
        ),
    ],
    fluid=True,
    className="p-4",
)

from app.callbacks import tab1_callbacks

if __name__ == "__main__":
    app.run_server(debug=True)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
