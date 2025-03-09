import dash_bootstrap_components as dbc
from dash import html
from app.utils.data_fetcher import fetch_lineup_data


def create_season_summary_cards(team_id):
    """Creates the season summary cards with the performance breakdown path."""
    draft_data = fetch_lineup_data(
        "leagues/47097656/teams/lineups/best-drafted", team_id
    )
    actual_best_data = fetch_lineup_data(
        "leagues/47097656/teams/lineups/best-actual", team_id
    )
    actual_lineup_data = fetch_lineup_data(
        "leagues/47097656/teams/lineups/actual", team_id
    )

    draft_baseline = sum(
        sum(player["points"] for pos in data["starters"].values() for player in pos)
        for week, data in draft_data.items()
    )

    best_possible = sum(
        sum(player["points"] for pos in data["starters"].values() for player in pos)
        for week, data in actual_best_data.items()
    )

    actual_points = sum(
        sum(player["points"] for pos in data["starters"].values() for player in pos)
        for week, data in actual_lineup_data.items()
    )

    # Count weeks for averaging
    num_weeks = len(draft_data.keys())

    # Convert to weekly averages if requested
    draft_baseline /= num_weeks
    best_possible /= num_weeks
    actual_points /= num_weeks

    # Calculate impacts
    transaction_impact = best_possible - draft_baseline
    lineup_impact = actual_points - best_possible

    # Create efficiency percentage
    lineup_efficiency = (
        (actual_points / best_possible * 100) if best_possible > 0 else 0
    )

    transaction_sign = "+" if transaction_impact > 0 else ""

    # Determine direction badges
    transaction_badge = {
        "text": "POSITIVE" if transaction_impact > 0 else "NEGATIVE",
        "color": "success" if transaction_impact > 0 else "danger",
    }

    # Create the stepped visual
    return dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # Step 1: Draft Baseline
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H5(
                                                    "Draft Baseline",
                                                    className="text-primary mb-1",
                                                ),
                                                html.H2(
                                                    f"{draft_baseline:.1f}",
                                                    className="text-primary fw-bold",
                                                ),
                                                html.P(
                                                    "pts/week",
                                                    className="mb-0 small",
                                                ),
                                                html.P(
                                                    "Best possible lineup with drafted roster",
                                                    className="text-muted small mb-0",
                                                ),
                                            ],
                                            className="border-start border-5 border-primary p-2 h-100",
                                        ),
                                    ],
                                    width=4,
                                    id="draft-baseline-card",
                                ),
                                # Step 2: Transaction Impact
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H5(
                                                    "Roster Management",
                                                    className="text-success mb-1",
                                                ),
                                                html.H2(
                                                    f"{best_possible:.1f}",
                                                    className="text-success fw-bold",
                                                ),
                                                html.P(
                                                    "pts/week",
                                                    className="mb-0 small",
                                                ),
                                                html.P(
                                                    "Best possible lineup with actual roster",
                                                    className="text-muted small mb-0",
                                                ),
                                            ],
                                            className="border-start border-5 border-success p-2 h-100",
                                        ),
                                    ],
                                    width=3,
                                    id="transaction-impact-card",
                                ),
                                # Transaction Impact Badge Column (new)
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Span(
                                                    [
                                                        html.I(
                                                            className=f"fas {'fa-plus' if transaction_impact > 0 else 'fa-minus'} me-2",
                                                        ),
                                                        f"{transaction_sign}{abs(transaction_impact):.1f} ",
                                                    ],
                                                    className=f"badge rounded-pill bg-{transaction_badge['color']} px-3 py-3",
                                                    style={
                                                        "font-size": "1.25rem",  # Bigger font
                                                    },
                                                ),
                                            ],
                                            className="d-flex align-items-center justify-content-end h-100 pe-2",
                                        ),
                                    ],
                                    width=1,
                                ),
                                # Step 3: Lineup Efficiency
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.H5(
                                                    "Lineup Efficiency",
                                                    className="text-warning mb-1",
                                                ),
                                                html.H2(
                                                    f"{actual_points:.1f}",
                                                    className="text-warning fw-bold",
                                                ),
                                                html.P(
                                                    "pts/week",
                                                    className="mb-0 small",
                                                ),
                                                html.P(
                                                    f"Actual selected lineup",
                                                    className="text-muted small mb-0",
                                                ),
                                            ],
                                            className="border-start border-5 border-warning p-2 h-100",
                                        ),
                                    ],
                                    width=3,
                                    id="lineup-efficiency-card",
                                ),
                                dbc.Col(
                                    [
                                        html.Div(
                                            [
                                                html.Span(
                                                    [
                                                        html.I(
                                                            className=f"fas {'fa-plus' if transaction_impact > 0 else 'fa-minus'} me-2"
                                                        ),
                                                        f"{lineup_efficiency:.0f}% ",
                                                    ],
                                                    className=f"badge rounded-pill bg-warning px-3 py-3",
                                                    style={
                                                        "font-size": "1.25rem",  # Bigger font
                                                    },
                                                ),
                                            ],
                                            className="d-flex align-items-center justify-content-end h-100 pe-2",
                                        ),
                                    ],
                                    width=1,
                                ),
                            ],
                            className="g-2 align-items-stretch",
                        ),
                        # Explanation text
                        html.Div(
                            [
                                html.P(
                                    [
                                        html.Strong("How to read this:"),
                                        " We start with your draft baseline (points if you never changed your roster), then show the impact of your transactions, then how efficiently you set your lineup each week.",
                                    ],
                                    className="text-muted small mt-3 mb-0",
                                )
                            ]
                        ),
                    ]
                )
            ],
            className="mb-4 shadow",
        ),
        width=11,
    )
