from dash.dependencies import Input, Output
from dash import callback_context
from app.components.season_line_charts import create_season_overview
from app.components.season_waterfall import create_season_waterfall
from app.components.summary_cards import create_season_summary_cards
from app.app import app


# Callbacks for Tab 1
@app.callback(
    [
        Output("season-overview-chart", "figure"),
        Output("season-summary-cards", "children"),
        Output("season-waterfall", "figure"),
    ],
    [
        Input("team-dropdown", "value"),
        Input("view-toggle", "value"),
        # Input("stat-type-toggle", "value"),
    ],
)
def update_season_overview(
    team_id,
    view_mode,
    # stat_type
):
    """Updates the season overview chart and summary cards"""
    season_chart = create_season_overview(team_id, view_mode)
    summary_cards = create_season_summary_cards(team_id)
    season_waterfall = create_season_waterfall(team_id, view_mode)
    return season_chart, summary_cards, season_waterfall
