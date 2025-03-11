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
    _, draft_points, _ = process_weekly_data(draft_data)
    _, actual_best_points, _ = process_weekly_data(actual_best_data)
    _, actual_lineup_points, _ = process_weekly_data(actual_lineup_data)

    # Calculate averages and impacts
    draft_points_avg = np.mean(draft_points)
    actual_best_points_avg = np.mean(actual_best_points)
    actual_lineup_points_avg = np.mean(actual_lineup_points)
    transaction_impact = actual_best_points_avg - draft_points_avg

    # Set bar colors
    colors = {
        "draft": "rgba(30, 144, 255, 0.8)",  # Blue for draft
        "positive": "rgba(46, 204, 113, 0.8)",  # Green for positive transactions
        "negative": "rgba(231, 76, 60, 0.8)",  # Red for negative transactions
        "actual": "rgba(241, 196, 15, 0.8)",  # Yellow for actual
        "missed": "rgba(241, 196, 15, 0.3)",  # Transparent yellow for unrealized
    }

    # Calculate efficiency percentage
    lineup_efficiency = (
        (actual_lineup_points_avg / actual_best_points_avg * 100)
        if actual_best_points_avg > 0
        else 0
    )
    efficiency_text = f"{lineup_efficiency:.0f}% Efficient"

    # Create a figure with subplots for custom layout
    fig = go.Figure()

    # Set x-positions and width
    x_positions = ["Draft Baseline", "Transactions", "Actual"]
    bar_width = 0.6

    # First bar: Draft Value
    fig.add_trace(
        go.Bar(
            x=[x_positions[0]],
            y=[draft_points_avg],
            name="Draft Baseline",
            marker_color=colors["draft"],
            width=bar_width,
            text=f"{draft_points_avg:.1f}",
            textposition="outside",
            hovertemplate="Draft Value: %{y:.1f} pts<br>Baseline weekly points if you never changed your roster<extra></extra>",
        )
    )

    # Second bar: Transaction Impact (only the impact, not the total)
    transaction_color = (
        colors["positive"] if transaction_impact > 0 else colors["negative"]
    )
    fig.add_trace(
        go.Bar(
            x=[x_positions[1]],
            y=[abs(transaction_impact)],  # Use absolute value for bar height
            name="Transaction Impact",
            marker_color=transaction_color,
            width=bar_width,
            text=f"{transaction_impact:+.1f}",
            textposition="outside",
            hovertemplate="Transaction Impact: %{text} pts<br>Effect of all your add/drops and trades<extra></extra>",
            base=[draft_points_avg],  # Base determines if bar goes up or down
        )
    )

    # Third bar: Actual Points (solid part)
    fig.add_trace(
        go.Bar(
            x=[x_positions[2]],
            y=[actual_lineup_points_avg],
            name="Actual Points",
            marker_color=colors["actual"],
            width=bar_width,
            text=f"{actual_lineup_points_avg:.1f}",
            # textposition="outside",
            hovertemplate="Actual Points: %{y:.1f} pts<br>Points actually scored<extra></extra>",
        )
    )

    # Fourth bar: Unrealized Potential (transparent extension)
    unrealized = actual_best_points_avg - actual_lineup_points_avg
    fig.add_trace(
        go.Bar(
            x=[x_positions[2]],
            y=[unrealized],
            base=[actual_lineup_points_avg],  # Start from top of actual points
            name="Unrealized Potential",
            marker=dict(
                color=colors["missed"],
                pattern=dict(shape="/"),  # Diagonal line pattern
            ),
            text=f"{actual_best_points_avg:.1f}",
            textposition="outside",
            width=bar_width,
            hovertemplate="Unrealized Potential: %{y:.1f} pts<br>Points left on the table due to lineup decisions<extra></extra>",
            showlegend=False,
        )
    )

    # Add a reference line for the draft value
    fig.add_shape(
        type="line",
        x0=-0.5,
        y0=draft_points_avg,
        x1=2.5,
        y1=draft_points_avg,
        line=dict(
            color="gray",
            width=1,
            dash="dot",
        ),
    )

    # # Add a reference line for the total potential
    fig.add_shape(
        type="line",
        x0=1.5,
        y0=actual_best_points_avg,
        x1=2.5,
        y1=actual_best_points_avg,
        line=dict(
            color="gray",
            width=1,
            dash="dot",
        ),
    )

    # Update layout
    fig.update_layout(
        title="Season Performance Breakdown",
        barmode="overlay",
        bargap=0.15,
        bargroupgap=0.1,
        plot_bgcolor="white",
        yaxis=dict(
            title="Weekly Points Average",
            gridcolor="lightgray",
            zerolinecolor="lightgray",
        ),
        xaxis=dict(title="", tickangle=0),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            itemwidth=30,
            traceorder="normal",
            font=dict(size=10),
        ),
        margin=dict(t=0, b=0, l=50, r=50),
        height=350,
        # annotations=[
        #     dict(
        #         x=0.5,
        #         y=-0.25,
        #         xref="paper",
        #         yref="paper",
        #         text="<b>How to read this:</b> First bar shows your draft value, second shows the impact of transactions, third shows actual points with unrealized potential",
        #         showarrow=False,
        #         font=dict(size=11),
        #         align="center",
        #     )
        # ],
    )

    return fig
