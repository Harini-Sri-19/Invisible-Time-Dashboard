"""
charts.py
----------
All Plotly figure construction lives here, fully themed to match the
"Invisible Time" dark, futuristic visual identity. Keeping chart-building
separate from app.py means the page-layout file stays clean and the
chart logic can be unit-tested or reused independently.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.theme import COLORS, CATEGORY_PALETTE

# Shared layout settings applied to every chart for visual consistency
BASE_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", color=COLORS["text_primary"], size=13),
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        font=dict(color=COLORS["text_secondary"], size=11),
        orientation="h",
        yanchor="bottom",
        y=-0.25,
        xanchor="center",
        x=0.5,
    ),
    hoverlabel=dict(
        bgcolor=COLORS["surface_alt"],
        font_color=COLORS["text_primary"],
        bordercolor=COLORS["border"],
    ),
)


def _apply_base_layout(fig: go.Figure, height: int = 360) -> go.Figure:
    fig.update_layout(**BASE_LAYOUT, height=height)
    fig.update_xaxes(showgrid=False, color=COLORS["text_secondary"], linecolor=COLORS["border"])
    fig.update_yaxes(
        showgrid=True,
        gridcolor=COLORS["grid_line"],
        color=COLORS["text_secondary"],
        zerolinecolor=COLORS["border"],
    )
    return fig


def category_donut(category_df: pd.DataFrame) -> go.Figure:
    """Donut chart showing where total time goes, split by category."""
    fig = go.Figure(
        data=[
            go.Pie(
                labels=category_df["Category"],
                values=category_df["Duration_Minutes"],
                hole=0.62,
                marker=dict(colors=CATEGORY_PALETTE, line=dict(color=COLORS["void"], width=2)),
                textinfo="percent",
                textfont=dict(color=COLORS["text_primary"], size=12),
                hovertemplate="<b>%{label}</b><br>%{value:.0f} min (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        showlegend=True,
        annotations=[
            dict(
                text="TIME<br>SPLIT",
                x=0.5, y=0.5,
                font=dict(size=14, color=COLORS["text_secondary"], family="JetBrains Mono"),
                showarrow=False,
            )
        ],
    )
    return _apply_base_layout(fig, height=380)


def top_activities_bar(top_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of the top time-draining activities."""
    sorted_df = top_df.sort_values("Hours")
    fig = go.Figure(
        data=[
            go.Bar(
                x=sorted_df["Hours"],
                y=sorted_df["Activity_Name"],
                orientation="h",
                marker=dict(
                    color=sorted_df["Hours"],
                    colorscale=[[0, COLORS["drift_blue"]], [1, COLORS["phantom_violet"]]],
                    line=dict(width=0),
                ),
                text=sorted_df["Hours"].astype(str) + " h",
                textposition="outside",
                textfont=dict(color=COLORS["text_primary"]),
                hovertemplate="<b>%{y}</b><br>%{x} hours<extra></extra>",
            )
        ]
    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title="Hours Spent")
    return _apply_base_layout(fig, height=380)


def hourly_pattern_area(hourly_df: pd.DataFrame) -> go.Figure:
    """Area chart showing the 24-hour rhythm of invisible time loss."""
    fig = go.Figure(
        data=[
            go.Scatter(
                x=hourly_df["Hour"],
                y=hourly_df["Total_Minutes"],
                mode="lines",
                fill="tozeroy",
                line=dict(color=COLORS["phantom_violet"], width=2.5, shape="spline"),
                fillcolor="rgba(167,139,250,0.18)",
                hovertemplate="Hour %{x}:00<br>%{y:.0f} minutes<extra></extra>",
            )
        ]
    )
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title="Hour of Day", dtick=2, tickmode="linear")
    fig.update_yaxes(title="Minutes Lost")
    return _apply_base_layout(fig, height=320)


def daily_trend_line(trend_df: pd.DataFrame) -> go.Figure:
    """Dual-line trend of productive vs non-productive minutes over time."""
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=trend_df["Date"], y=trend_df["Non-Productive"],
            mode="lines", name="Non-Productive",
            line=dict(color=COLORS["phantom_violet"], width=2),
            hovertemplate="%{x|%b %d}<br>%{y:.0f} min<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=trend_df["Date"], y=trend_df["Productive"],
            mode="lines", name="Productive",
            line=dict(color=COLORS["ghost_cyan"], width=2),
            hovertemplate="%{x|%b %d}<br>%{y:.0f} min<extra></extra>",
        )
    )
    fig.update_xaxes(title=None)
    fig.update_yaxes(title="Minutes")
    return _apply_base_layout(fig, height=340)


def weekday_radial_bar(weekday_df: pd.DataFrame) -> go.Figure:
    """Bar chart highlighting which weekday tends to leak the most time."""
    max_idx = weekday_df["Avg_Minutes"].idxmax()
    colors = [
        COLORS["rose_alert"] if i == max_idx else COLORS["drift_blue"]
        for i in range(len(weekday_df))
    ]
    fig = go.Figure(
        data=[
            go.Bar(
                x=weekday_df["Day"].str[:3],
                y=weekday_df["Avg_Minutes"],
                marker=dict(color=colors, line=dict(width=0)),
                hovertemplate="<b>%{x}</b><br>%{y:.0f} min avg<extra></extra>",
            )
        ]
    )
    fig.update_layout(showlegend=False)
    fig.update_yaxes(title="Avg Minutes / Day")
    return _apply_base_layout(fig, height=320)


def productivity_gauge(ratio: dict) -> go.Figure:
    """Gauge-style indicator showing the productive percentage of time."""
    value = ratio.get("Productive", 0)
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            number=dict(suffix="%", font=dict(size=34, color=COLORS["text_primary"], family="Space Grotesk")),
            gauge=dict(
                axis=dict(range=[0, 100], tickcolor=COLORS["text_secondary"], tickfont=dict(size=10)),
                bar=dict(color=COLORS["ghost_cyan"], thickness=0.28),
                bgcolor="rgba(0,0,0,0)",
                borderwidth=0,
                steps=[
                    dict(range=[0, 40], color="rgba(251,113,133,0.18)"),
                    dict(range=[40, 70], color="rgba(251,191,36,0.15)"),
                    dict(range=[70, 100], color="rgba(94,234,212,0.15)"),
                ],
            ),
        )
    )
    return _apply_base_layout(fig, height=260)


def category_treemap(category_df: pd.DataFrame) -> go.Figure:
    """Treemap as an alternative dense view of category time allocation."""
    fig = go.Figure(
        go.Treemap(
            labels=category_df["Category"],
            parents=["" for _ in range(len(category_df))],
            values=category_df["Duration_Minutes"],
            marker=dict(colors=CATEGORY_PALETTE, line=dict(color=COLORS["void"], width=2)),
            textinfo="label+percent root",
            textfont=dict(color=COLORS["text_primary"], size=13),
            hovertemplate="<b>%{label}</b><br>%{value:.0f} min<extra></extra>",
        )
    )
    return _apply_base_layout(fig, height=380)
