import numpy as np
import logging
import plotly.graph_objects as go
from app.utils.data_fetcher import fetch_lineup_data
from app.utils.data_processor import process_weekly_data

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_season_waterfall(team_id, view_mode="all"):
    """Creates the season performance waterfall chart with toggle options"""
    logger.info(
        f"Creating season overview for team {team_id} with view mode: {view_mode}"
    )

    # Fetch data for all three scenarios
    draft_data = fetch_lineup_data(
        "leagues/47097656/teams/lineups/best-drafted", team_id
    )
    actual_best_data = fetch_lineup_data(
        "leagues/47097656/teams/lineups/best-actual", team_id
    )
    actual_lineup_data = fetch_lineup_data(
        "leagues/47097656/teams/lineups/actual", team_id
    )

    # Process data for all three scenarios
    draft_weeks, draft_points, draft_hover = process_weekly_data(draft_data)
    actual_best_weeks, actual_best_points, actual_best_hover = process_weekly_data(
        actual_best_data
    )
    actual_lineup_weeks, actual_lineup_points, actual_lineup_hover = (
        process_weekly_data(actual_lineup_data)
    )

    draft_points_avg = np.mean(draft_points)
    actual_best_points_avg = np.mean(actual_best_points)
    actual_lineup_points_avg = np.mean(actual_lineup_points)
    transaction_impact = actual_best_points_avg - draft_points_avg
    lineup_decision_impact = actual_lineup_points_avg - actual_best_points_avg

    waterfall_fig = go.Figure(
        go.Waterfall(
            name="Decision Impact",
            orientation="v",
            measure=["absolute", "relative", "relative", "total"],
            x=["Draft Value", "Transactions", "Lineup Decisions", "Actual Points"],
            textposition="outside",
            text=[
                f"{draft_points_avg:.1f}",
                f"{transaction_impact:+.1f}",
                f"{lineup_decision_impact:+.1f}",
                f"{actual_lineup_points_avg:.1f}",
            ],
            y=[
                draft_points_avg,
                transaction_impact,
                lineup_decision_impact,
                actual_lineup_points_avg,
            ],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            decreasing={"marker": {"color": "red"}},
            increasing={"marker": {"color": "green"}},
            totals={"marker": {"color": "blue"}},
        )
    )

    waterfall_fig.update_layout(
        title=f"Performance Components Breakdown",
        xaxis_title="Components",
        yaxis_title="Points",
        showlegend=False,
    )
    return waterfall_fig


# TODO: Implement new waterfall
# def create_season_waterfall(team_id, view_mode="roster_comparison"):
#     """Creates a waterfall chart showing the performance breakdown."""
#     # Fetch your data here based on team_id
#     # These are placeholder values - replace with your actual data
#     draft_baseline = 110.5  # Avg points from draft-only lineup
#     best_possible = 125.2  # Avg points from best possible roster after transactions
#     actual_points = 95.8  # Avg actual points scored

#     # Calculate impacts
#     transaction_impact = best_possible - draft_baseline
#     lineup_impact = actual_points - best_possible

#     # Create the waterfall chart
#     fig = go.Figure()

#     # Define colors to match summary cards
#     colors = {
#         "baseline": "rgba(13, 110, 253, 0.8)",  # Primary/blue for draft
#         "positive": "rgba(40, 167, 69, 0.8)",  # Success/green for good transactions
#         "negative": "rgba(220, 53, 69, 0.8)",  # Danger/red for bad transactions
#         "lineup": "rgba(255, 193, 7, 0.8)",  # Warning/yellow for lineup efficiency
#         "final": "rgba(23, 162, 184, 0.8)",  # Info/teal for final score
#     }

#     # Add measures
#     fig.add_trace(
#         go.Waterfall(
#             name="Performance Breakdown",
#             orientation="v",
#             measure=["absolute", "relative", "relative", "total"],
#             x=[
#                 "Draft Baseline",
#                 "Transaction Impact",
#                 "Lineup Decisions",
#                 "Final Score",
#             ],
#             textposition="outside",
#             y=[draft_baseline, transaction_impact, lineup_impact, 0],
#             text=[
#                 f"{draft_baseline:.1f}",
#                 f"{transaction_impact:+.1f}",
#                 f"{lineup_impact:+.1f}",
#                 f"{actual_points:.1f}",
#             ],
#             connector={"line": {"color": "rgb(63, 63, 63)"}},
#             increasing={"marker": {"color": colors["positive"]}},
#             decreasing={"marker": {"color": colors["negative"]}},
#             totals={"marker": {"color": colors["final"]}},
#         )
#     )

#     # Calculate percentages for annotations
#     total_abs_impact = abs(transaction_impact) + abs(lineup_impact)
#     trans_pct = (
#         abs(transaction_impact) / total_abs_impact * 100 if total_abs_impact > 0 else 0
#     )
#     lineup_pct = (
#         abs(lineup_impact) / total_abs_impact * 100 if total_abs_impact > 0 else 0
#     )

#     # Add annotations explaining percentages
#     fig.add_annotation(
#         x="Transaction Impact",
#         y=draft_baseline + transaction_impact / 2,
#         text=f"{trans_pct:.0f}% of total impact",
#         showarrow=False,
#         font=dict(color="white" if trans_pct > 15 else "black", size=10),
#         bgcolor="rgba(0,0,0,0.3)" if trans_pct > 15 else None,
#         borderpad=4 if trans_pct > 15 else 0,
#     )

#     fig.add_annotation(
#         x="Lineup Decisions",
#         y=draft_baseline + transaction_impact + lineup_impact / 2,
#         text=f"{lineup_pct:.0f}% of total impact",
#         showarrow=False,
#         font=dict(color="white" if lineup_pct > 15 else "black", size=10),
#         bgcolor="rgba(0,0,0,0.3)" if lineup_pct > 15 else None,
#         borderpad=4 if lineup_pct > 15 else 0,
#     )

#     # Update layout
#     fig.update_layout(
#         title={"text": "Season Performance Breakdown", "x": 0.5, "xanchor": "center"},
#         showlegend=False,
#         xaxis={
#             "title": None,
#             "tickangle": 0,
#         },
#         yaxis={
#             "title": "Average Points Per Week",
#             "ticksuffix": " pts",
#             "gridcolor": "rgba(0,0,0,0.1)",
#         },
#         margin={"t": 50, "b": 70, "l": 50, "r": 50},
#         height=400,
#         template="plotly_white",
#         annotations=[
#             dict(
#                 x=0.5,
#                 y=-0.15,
#                 xref="paper",
#                 yref="paper",
#                 text="<b>How to read this:</b> We start with your draft baseline, add/subtract transaction impact, then lineup efficiency to get your final score",
#                 showarrow=False,
#                 font=dict(size=11),
#                 align="center",
#             )
#         ],
#     )

#     return fig
