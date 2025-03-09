import plotly.graph_objs as go
import numpy as np
import logging
from app.utils.data_fetcher import fetch_lineup_data
from app.utils.data_processor import process_weekly_data


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_season_overview(team_id, view_mode="roster_comparison"):
    """
    Creates a season overview chart with toggle options

    Args:
        team_id: The team ID to fetch data for
        view_mode: Either "roster_comparison" or "lineup_comparison"

    Returns:
        A plotly figure object
    """
    logger.info(
        f"Creating season overview for team {team_id} with view mode: {view_mode}"
    )

    # Fetch and process data
    data = fetch_chart_data(team_id)

    # Create the base figure
    fig = go.Figure()

    # Add appropriate chart elements based on view mode
    if view_mode == "roster_comparison":
        add_roster_comparison_elements(fig, data)
    elif view_mode == "lineup_comparison":
        add_lineup_comparison_elements(fig, data)

    # Apply common layout settings
    apply_common_layout(fig, data, view_mode)

    return fig


def fetch_chart_data(team_id):
    """Fetches and processes all data needed for the charts"""
    # Fetch data for all scenarios
    draft_data = fetch_lineup_data(
        "leagues/47097656/teams/lineups/best-drafted", team_id
    )
    actual_best_data = fetch_lineup_data(
        "leagues/47097656/teams/lineups/best-actual", team_id
    )
    actual_lineup_data = fetch_lineup_data(
        "leagues/47097656/teams/lineups/actual", team_id
    )

    # Process data
    draft_weeks, draft_points, draft_hover = process_weekly_data(draft_data)
    actual_best_weeks, actual_best_points, actual_best_hover = process_weekly_data(
        actual_best_data
    )
    actual_lineup_weeks, actual_lineup_points, actual_lineup_hover = (
        process_weekly_data(actual_lineup_data)
    )

    # Calculate averages
    avg_draft = np.mean(draft_points)
    avg_actual_best = np.mean(actual_best_points)
    avg_actual_lineup = np.mean(actual_lineup_points)

    # Calculate efficiency percentages
    lineup_efficiency = [
        (actual / best) * 100 if best > 0 else 0
        for actual, best in zip(actual_lineup_points, actual_best_points)
    ]
    avg_efficiency = np.mean(lineup_efficiency)

    # Calculate weekly differences (for roster comparison)
    weekly_diffs = [
        actual - draft for actual, draft in zip(actual_best_points, draft_points)
    ]

    # Calculate y-axis range
    all_points = draft_points + actual_best_points + actual_lineup_points
    min_points = min(all_points)
    y_min = min(80, min_points * 0.8)  # 80% of min or 80, whichever is smaller
    y_max = max(all_points) * 1.1  # Add 10% padding above highest value

    # Return all data in a dictionary
    return {
        "draft_weeks": draft_weeks,
        "draft_points": draft_points,
        # "draft_hover": draft_hover,
        "actual_best_weeks": actual_best_weeks,
        "actual_best_points": actual_best_points,
        # "actual_best_hover": actual_best_hover,
        "actual_lineup_weeks": actual_lineup_weeks,
        "actual_lineup_points": actual_lineup_points,
        # "actual_lineup_hover": actual_lineup_hover,
        "avg_draft": avg_draft,
        "avg_actual_best": avg_actual_best,
        "avg_actual_lineup": avg_actual_lineup,
        "lineup_efficiency": lineup_efficiency,
        "avg_efficiency": avg_efficiency,
        "weekly_diffs": weekly_diffs,
        "y_min": y_min,
        "y_max": y_max,
    }


def add_roster_comparison_elements(fig, data):
    """Adds all elements needed for roster comparison view"""
    # Unpack data
    draft_weeks = data["draft_weeks"]
    draft_points = data["draft_points"]
    actual_best_weeks = data["actual_best_weeks"]
    actual_best_points = data["actual_best_points"]
    avg_draft = data["avg_draft"]
    avg_actual_best = data["avg_actual_best"]
    weekly_diffs = data["weekly_diffs"]

    # Add main line traces
    add_main_lines_roster(
        fig, draft_weeks, draft_points, actual_best_weeks, actual_best_points
    )

    # Add fill areas between lines
    add_fill_areas_roster(fig, draft_weeks, draft_points, actual_best_points)

    # Add average lines
    add_average_lines_roster(
        fig, draft_weeks, actual_best_weeks, avg_draft, avg_actual_best
    )

    # Add hover data
    add_hover_data_roster(
        fig, draft_weeks, draft_points, actual_best_points, weekly_diffs
    )

    # Add annotations
    annotations = create_annotations_roster(
        draft_weeks, actual_best_weeks, avg_draft, avg_actual_best
    )

    # Set chart title and subtitle
    title_text = "Season Performance: Drafted vs. Actual Roster Comparison"
    subtitle = "Green areas show weeks with positive transaction impact, red areas show negative impact"

    # Return title, subtitle, and annotations for layout
    return title_text, subtitle, annotations


def add_lineup_comparison_elements(fig, data):
    """Adds all elements needed for lineup comparison view"""
    # Unpack data
    actual_best_weeks = data["actual_best_weeks"]
    actual_best_points = data["actual_best_points"]
    actual_lineup_weeks = data["actual_lineup_weeks"]
    actual_lineup_points = data["actual_lineup_points"]
    avg_actual_best = data["avg_actual_best"]
    avg_actual_lineup = data["avg_actual_lineup"]
    lineup_efficiency = data["lineup_efficiency"]
    avg_efficiency = data["avg_efficiency"]

    # Add main line traces
    add_main_lines_lineup(
        fig,
        actual_best_weeks,
        actual_best_points,
        actual_lineup_weeks,
        actual_lineup_points,
    )

    # Add fill areas
    add_fill_areas_lineup(
        fig,
        actual_best_weeks,
        actual_best_points,
        actual_lineup_weeks,
        actual_lineup_points,
    )

    # Add average lines
    add_average_lines_lineup(
        fig, actual_best_weeks, actual_lineup_weeks, avg_actual_best, avg_actual_lineup
    )

    # Add hover data
    add_hover_data_lineup(
        fig,
        actual_lineup_weeks,
        actual_lineup_points,
        actual_best_points,
        lineup_efficiency,
    )

    # Add annotations
    annotations = create_annotations_lineup(
        actual_best_weeks,
        actual_lineup_weeks,
        avg_actual_best,
        avg_actual_lineup,
        avg_efficiency,
    )

    # Set chart title and subtitle
    title_text = "Season Performance: Lineup Decision Comparison"
    subtitle = "Red areas show potential points left on the bench, green areas show points achieved"

    # Return title, subtitle, and annotations for layout
    return title_text, subtitle, annotations


def add_main_lines_roster(
    fig, draft_weeks, draft_points, actual_best_weeks, actual_best_points
):
    """Adds the main line traces for roster comparison view"""
    # Add drafted team line
    fig.add_trace(
        go.Scatter(
            x=draft_weeks,
            y=draft_points,
            mode="lines+markers",
            name="Best possible lineup",
            line=dict(color="blue", width=2),
            marker=dict(size=8),
            legendgroup="draft",
            legendgrouptitle_text="Drafted Team Performance",
            hoverinfo="skip",
        )
    )

    # Add actual best roster line
    fig.add_trace(
        go.Scatter(
            x=actual_best_weeks,
            y=actual_best_points,
            mode="lines+markers",
            name="Best possible lineup",
            line=dict(color="green", width=2),
            marker=dict(size=8),
            legendgroup="actual",
            legendgrouptitle_text="Actual Team Performance",
            hoverinfo="skip",
        )
    )


def add_fill_areas_roster(fig, draft_weeks, draft_points, actual_best_points):
    """Adds fill areas between lines for roster comparison view"""
    # First, draw the positive fill areas (where actual best is above draft best)
    positive_x = []
    positive_y_upper = []
    positive_y_lower = []

    # Then, draw the negative fill areas (where draft best is above actual best)
    negative_x = []
    negative_y_upper = []
    negative_y_lower = []

    # Process each pair of adjacent points to determine appropriate fill
    for i in range(len(draft_weeks) - 1):
        x1, x2 = draft_weeks[i], draft_weeks[i + 1]
        y1_draft, y2_draft = draft_points[i], draft_points[i + 1]
        y1_actual, y2_actual = actual_best_points[i], actual_best_points[i + 1]

        # Check if lines cross between these points
        lines_cross = ((y1_draft > y1_actual) and (y2_draft < y2_actual)) or (
            (y1_draft < y1_actual) and (y2_draft > y2_actual)
        )

        if lines_cross:
            # Calculate intersection point
            # Line equation: y = mx + b
            m1 = (y2_draft - y1_draft) / (x2 - x1)
            b1 = y1_draft - m1 * x1

            m2 = (y2_actual - y1_actual) / (x2 - x1)
            b2 = y1_actual - m2 * x1

            # Intersection: m1*x + b1 = m2*x + b2 => x = (b2 - b1) / (m1 - m2)
            if m1 != m2:  # Avoid division by zero
                x_intersect = (b2 - b1) / (m1 - m2)
                y_intersect = m1 * x_intersect + b1

                # Add segments to appropriate arrays based on which line is on top
                if y1_draft < y1_actual:  # First part is positive
                    # Add positive segment
                    positive_x.extend([x1, x_intersect])
                    positive_y_upper.extend([y1_actual, y_intersect])
                    positive_y_lower.extend([y1_draft, y_intersect])

                    # Add negative segment
                    negative_x.extend([x_intersect, x2])
                    negative_y_upper.extend([y_intersect, y2_draft])
                    negative_y_lower.extend([y_intersect, y2_actual])
                else:  # First part is negative
                    # Add negative segment
                    negative_x.extend([x1, x_intersect])
                    negative_y_upper.extend([y1_draft, y_intersect])
                    negative_y_lower.extend([y1_actual, y_intersect])

                    # Add positive segment
                    positive_x.extend([x_intersect, x2])
                    positive_y_upper.extend([y_intersect, y2_actual])
                    positive_y_lower.extend([y_intersect, y2_draft])
        else:
            # No crossing, add entire segment to appropriate array
            if y1_actual >= y1_draft and y2_actual >= y2_draft:  # Positive throughout
                positive_x.extend([x1, x2])
                positive_y_upper.extend([y1_actual, y2_actual])
                positive_y_lower.extend([y1_draft, y2_draft])
            elif y1_draft >= y1_actual and y2_draft >= y2_actual:  # Negative throughout
                negative_x.extend([x1, x2])
                negative_y_upper.extend([y1_draft, y2_draft])
                negative_y_lower.extend([y1_actual, y2_actual])
            else:
                # This shouldn't happen if we correctly detected crossings
                logger.warning(f"Unexpected line configuration at week {x1}")

    # Add positive fill areas
    if positive_x:
        # Create a continuous path for fill: go forward along upper line, then backward along lower line
        x_path = positive_x + positive_x[::-1]
        y_path = positive_y_upper + positive_y_lower[::-1]

        fig.add_trace(
            go.Scatter(
                x=x_path,
                y=y_path,
                fill="toself",
                fillcolor="rgba(0, 255, 0, 0.2)",  # Green for good transactions
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                showlegend=False,
                legendgroup="fill_areas",
                name="Positive impact areas",
            )
        )

    # Add negative fill areas
    if negative_x:
        # Create a continuous path for fill: go forward along upper line, then backward along lower line
        x_path = negative_x + negative_x[::-1]
        y_path = negative_y_upper + negative_y_lower[::-1]

        fig.add_trace(
            go.Scatter(
                x=x_path,
                y=y_path,
                fill="toself",
                fillcolor="rgba(255, 0, 0, 0.2)",  # Red for bad transactions
                line=dict(color="rgba(255,255,255,0)"),
                hoverinfo="skip",
                showlegend=False,
                legendgroup="fill_areas",
                name="Negative impact areas",
            )
        )


def add_average_lines_roster(
    fig, draft_weeks, actual_best_weeks, avg_draft, avg_actual_best
):
    """Adds average lines for roster comparison view"""
    # Add horizontal average lines with hover text
    fig.add_trace(
        go.Scatter(
            x=[min(draft_weeks), max(draft_weeks)],
            y=[avg_draft, avg_draft],
            mode="lines",
            line=dict(color="blue", dash="dash", width=1),
            name="Season average",
            hovertemplate="Best drafted team average: %{y:.1f} pts<extra></extra>",
            legendgroup="draft",
            legendgrouptitle_text="Drafted Team Performance",
            showlegend=True,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[min(actual_best_weeks), max(actual_best_weeks)],
            y=[avg_actual_best, avg_actual_best],
            mode="lines",
            line=dict(color="green", dash="dash", width=1),
            name="Season average",
            hovertemplate="Best actual team average: %{y:.1f} pts<extra></extra>",
            legendgroup="actual",
            legendgrouptitle_text="Actual Team Performance",
            showlegend=True,
        )
    )


def add_hover_data_roster(
    fig, draft_weeks, draft_points, actual_best_points, weekly_diffs
):
    """Adds hover data for roster comparison view"""
    # Add week-by-week hover data (invisible trace that only appears on hover)
    hover_text = []
    for i, week in enumerate(draft_weeks):
        diff = weekly_diffs[i]
        diff_sign = "+" if diff > 0 else ""
        hover_text.append(
            f"<b>Week {week}</b><br>"
            f"Best drafted: {draft_points[i]:.1f} pts<br>"
            f"Best actual: {actual_best_points[i]:.1f} pts<br>"
            f"Difference: {diff_sign}{diff:.1f} pts"
        )

    fig.add_trace(
        go.Scatter(
            x=draft_weeks,
            y=[0] * len(draft_weeks),  # Invisible points - doesn't matter where
            mode="markers",
            marker=dict(size=0, opacity=0),  # Invisible
            hoverinfo="text",
            hovertext=hover_text,
            showlegend=False,
            name="hover_data",
        )
    )


def create_annotations_roster(
    draft_weeks, actual_best_weeks, avg_draft, avg_actual_best
):
    """Creates annotations for roster comparison view"""
    annotations = []

    # Calculate vertical positions to prevent overlap
    avg_values = [avg_draft, avg_actual_best]
    vertical_positions = position_annotations(avg_values, min_gap=7)

    # Add average annotations with hover info
    annotations.append(
        dict(
            x=max(draft_weeks) + 0.5,
            y=vertical_positions[0],
            xref="x",
            yref="y",
            text=f"Avg: {avg_draft:.1f}",
            showarrow=False,
            font=dict(color="blue", size=10),
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="blue",
            borderwidth=1,
            borderpad=3,
            xanchor="left",
            hovertext="Best draft lineup average",
            hoverlabel=dict(bgcolor="blue"),
        )
    )

    annotations.append(
        dict(
            x=max(actual_best_weeks) + 0.5,
            y=vertical_positions[1],
            xref="x",
            yref="y",
            text=f"Avg: {avg_actual_best:.1f}",
            showarrow=False,
            font=dict(color="green", size=10),
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="green",
            borderwidth=1,
            borderpad=3,
            xanchor="left",
            hovertext="Best actual lineup average",
            hoverlabel=dict(bgcolor="green"),
        )
    )

    return annotations


def add_main_lines_lineup(
    fig,
    actual_best_weeks,
    actual_best_points,
    actual_lineup_weeks,
    actual_lineup_points,
):
    """Adds main line traces for lineup comparison view"""
    # Add actual best roster line
    fig.add_trace(
        go.Scatter(
            x=actual_best_weeks,
            y=actual_best_points,
            mode="lines+markers",
            name="Best possible lineup",
            line=dict(color="green", width=2),
            marker=dict(size=8),
            legendgroup="best",
            legendgrouptitle_text="Best Possible Team Performance",
            hoverinfo="skip",
        )
    )

    # Add actual lineup performance line
    fig.add_trace(
        go.Scatter(
            x=actual_lineup_weeks,
            y=actual_lineup_points,
            mode="lines+markers",
            name="Actual lineup",
            line=dict(color="orange", width=3),
            marker=dict(size=10),
            legendgroup="actual",
            legendgrouptitle_text="Actual Team Performance",
            hoverinfo="skip",
        )
    )


def add_fill_areas_lineup(
    fig,
    actual_best_weeks,
    actual_best_points,
    actual_lineup_weeks,
    actual_lineup_points,
):
    """Adds fill areas for lineup comparison view"""
    # Fill between best actual and actual lineup with pattern (points left on bench)
    fig.add_trace(
        go.Scatter(
            x=actual_best_weeks + actual_best_weeks[::-1],
            y=actual_best_points + actual_lineup_points[::-1],
            fill="toself",
            fillcolor="rgba(255, 0, 0, 0.2)",  # Transparent red
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=False,
            name="Points left on bench",
            legendgroup="fill_areas",
        )
    )

    # Fill between actual lineup and zero (points achieved)
    fig.add_trace(
        go.Scatter(
            x=actual_lineup_weeks + actual_lineup_weeks[::-1],
            y=actual_lineup_points
            + [0] * len(actual_lineup_weeks),  # Bottom is zero line
            fill="toself",
            fillcolor="rgba(0, 255, 0, 0.1)",  # Transparent light green
            line=dict(color="rgba(255,255,255,0)"),
            hoverinfo="skip",
            showlegend=False,
            name="Points achieved",
            legendgroup="fill_areas",
        )
    )


def add_average_lines_lineup(
    fig, actual_best_weeks, actual_lineup_weeks, avg_actual_best, avg_actual_lineup
):
    """Adds average lines for lineup comparison view"""
    # Add horizontal average lines with hover text
    fig.add_trace(
        go.Scatter(
            x=[min(actual_best_weeks), max(actual_best_weeks)],
            y=[avg_actual_best, avg_actual_best],
            mode="lines",
            line=dict(color="green", dash="dash", width=1),
            name="Season average",
            hovertemplate="Best possible lineup average: %{y:.1f} pts<extra></extra>",
            legendgroup="best",
            legendgrouptitle_text="Best Possible Team Performance",
            showlegend=True,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[min(actual_lineup_weeks), max(actual_lineup_weeks)],
            y=[avg_actual_lineup, avg_actual_lineup],
            mode="lines",
            line=dict(color="orange", dash="dash", width=1),
            name="Season average",
            hovertemplate="Actual lineup average: %{y:.1f} pts<extra></extra>",
            legendgroup="actual",
            legendgrouptitle_text="Actual Team Performance",
            showlegend=True,
        )
    )


def add_hover_data_lineup(
    fig,
    actual_lineup_weeks,
    actual_lineup_points,
    actual_best_points,
    lineup_efficiency,
):
    """Adds hover data for lineup comparison view"""
    # Add week-by-week hover data (invisible trace that only appears on hover)
    hover_text = []
    for i, week in enumerate(actual_lineup_weeks):
        pct = lineup_efficiency[i]
        hover_text.append(
            f"<b>Week {week}</b><br>"
            f"Actual: {actual_lineup_points[i]:.1f} pts<br>"
            f"Best possible: {actual_best_points[i]:.1f} pts<br>"
            f"Efficiency: {pct:.1f}%"
        )

    fig.add_trace(
        go.Scatter(
            x=actual_lineup_weeks,
            y=[0] * len(actual_lineup_weeks),  # Invisible points
            mode="markers",
            marker=dict(size=0, opacity=0),  # Invisible
            hoverinfo="text",
            hovertext=hover_text,
            showlegend=False,
            name="hover_data",
        )
    )


def create_annotations_lineup(
    actual_best_weeks,
    actual_lineup_weeks,
    avg_actual_best,
    avg_actual_lineup,
    avg_efficiency,
):
    """Creates annotations for lineup comparison view"""
    annotations = []

    # Calculate vertical positions to prevent overlap
    avg_values = [avg_actual_best, avg_actual_lineup, avg_efficiency]
    vertical_positions = position_annotations(avg_values, min_gap=7)

    # Add average annotations with hover info
    annotations.append(
        dict(
            x=max(actual_best_weeks) + 0.5,
            y=vertical_positions[0],
            xref="x",
            yref="y",
            text=f"Avg: {avg_actual_best:.1f}",
            showarrow=False,
            font=dict(color="green", size=10),
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="green",
            borderwidth=1,
            borderpad=3,
            xanchor="left",
            hovertext="Best possible lineup average",
            hoverlabel=dict(bgcolor="green"),
        )
    )

    annotations.append(
        dict(
            x=max(actual_lineup_weeks) + 0.5,
            y=vertical_positions[1],
            xref="x",
            yref="y",
            text=f"Avg: {avg_actual_lineup:.1f}",
            showarrow=False,
            font=dict(color="orange", size=10),
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="orange",
            borderwidth=1,
            borderpad=3,
            xanchor="left",
            hovertext="Actual lineup average",
            hoverlabel=dict(bgcolor="orange"),
        )
    )

    annotations.append(
        dict(
            x=max(actual_lineup_weeks) + 0.5,
            y=vertical_positions[2],  # Adjusted position
            xref="x",
            yref="y",
            text=f"Avg Efficiency: {avg_efficiency:.1f}%",
            showarrow=False,
            font=dict(color="purple", size=10),
            bgcolor="rgba(255,255,255,0.7)",
            bordercolor="purple",
            borderwidth=1,
            borderpad=3,
            xanchor="left",
            hovertext="Average lineup efficiency",
            hoverlabel=dict(bgcolor="purple"),
        )
    )

    return annotations


def apply_common_layout(fig, data, view_mode):
    """Applies common layout settings to the chart"""
    # Get title and subtitle based on view mode
    if view_mode == "roster_comparison":
        title_text = "Season Performance: Drafted vs. Actual Roster Comparison"
        subtitle = "Green areas show weeks with positive transaction impact, red areas show negative impact"
    else:  # lineup_comparison
        title_text = "Season Performance: Lineup Decision Comparison"
        subtitle = "Red areas show potential points left on the bench, green areas show points achieved"

    # Calculate vertical positions for annotations to prevent overlap
    if view_mode == "roster_comparison":
        annotations = create_annotations_roster(
            data["draft_weeks"],
            data["actual_best_weeks"],
            data["avg_draft"],
            data["avg_actual_best"],
        )
    else:
        annotations = create_annotations_lineup(
            data["actual_best_weeks"],
            data["actual_lineup_weeks"],
            data["avg_actual_best"],
            data["avg_actual_lineup"],
            data["avg_efficiency"],
        )

    # Update layout
    fig.update_layout(
        title={
            "text": f"{title_text}<br><span style='font-size:12px; color:gray'>{subtitle}</span>",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
        },
        xaxis=dict(
            title=dict(
                text="Week",
                standoff=20,  # Add space for legend below
            ),
            tickmode="linear",
            tick0=1,
            dtick=1,
            range=[min(data["draft_weeks"]) - 0.5, max(data["draft_weeks"]) + 1.5],
            showspikes=True,  # Enable spike lines
            spikemode="across",
            spikesnap="cursor",
            spikecolor="gray",
            spikethickness=1,
        ),
        yaxis=dict(
            title="Points",
            side="left",
            range=[
                data["y_min"],
                data["y_max"],
            ],  # Set y-axis range to start at 80 or lower
        ),
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="Arial",
            bordercolor="gray",
            namelength=-1,  # Show full trace name
        ),
        hoverdistance=10,  # Make it tightly bound to points
        spikedistance=10,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.5,  # Position below x-axis title (moved further down)
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1,
            itemsizing="constant",
            itemwidth=40,
            tracegroupgap=20,
            groupclick="toggleitem",  # Toggle all items in group when legend is clicked
            # itemclick=False,  # Toggle single items when clicking directly on them
        ),
        clickmode="event+select",
        template="plotly_white",
        annotations=annotations,
        margin=dict(b=170, r=120),  # Increased bottom and right margins
    )


def position_annotations(values, min_gap=7):
    """
    Position annotations to prevent overlap.

    Args:
        values: List of values to position vertically
        min_gap: Minimum gap between annotations

    Returns:
        List of vertical positions for annotations
    """
    # Create a copy to avoid modifying the original
    positions = values.copy()

    # Sort positions
    sorted_indices = sorted(range(len(positions)), key=lambda i: positions[i])
    sorted_positions = [positions[i] for i in sorted_indices]

    # Ensure minimum gap between positions
    for i in range(1, len(sorted_positions)):
        if sorted_positions[i] - sorted_positions[i - 1] < min_gap:
            sorted_positions[i] = sorted_positions[i - 1] + min_gap

    # Remap back to original order
    result = [0] * len(positions)
    for i, idx in enumerate(sorted_indices):
        result[idx] = sorted_positions[i]

    return result
