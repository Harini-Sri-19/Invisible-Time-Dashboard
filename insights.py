"""
insights.py
------------
Pure functions that turn the cleaned dataframe into the metrics,
summaries, and "insight" sentences shown on the dashboard.

Kept separate from app.py so the analytical logic can be tested
or reused independently of the Streamlit UI layer.
"""

from __future__ import annotations

import pandas as pd


def total_hours_lost(df: pd.DataFrame, flag: str = "Non-Productive") -> float:
    """Total hours spent on activities matching the given productivity flag."""
    minutes = df.loc[df["Productivity_Flag"] == flag, "Duration_Minutes"].sum()
    return round(minutes / 60, 1)


def daily_average_minutes(df: pd.DataFrame, flag: str = "Non-Productive") -> float:
    """Average minutes per day lost to a given flag, across all logged days."""
    subset = df.loc[df["Productivity_Flag"] == flag]
    if subset.empty:
        return 0.0
    per_day = subset.groupby("Date")["Duration_Minutes"].sum()
    return round(per_day.mean(), 1)


def top_time_draining_activities(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Top-N activities by total time spent, non-productive only."""
    subset = df.loc[df["Productivity_Flag"] == "Non-Productive"]
    grouped = (
        subset.groupby("Activity_Name")["Duration_Minutes"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
    grouped["Hours"] = (grouped["Duration_Minutes"] / 60).round(1)
    return grouped


def category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Total minutes per category, used for pie / treemap visuals."""
    grouped = (
        df.groupby("Category")["Duration_Minutes"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    grouped["Hours"] = (grouped["Duration_Minutes"] / 60).round(1)
    grouped["Percentage"] = (grouped["Duration_Minutes"] / grouped["Duration_Minutes"].sum() * 100).round(1)
    return grouped


def hourly_distribution(df: pd.DataFrame, flag: str | None = "Non-Productive") -> pd.DataFrame:
    """Total minutes spent per hour-of-day bucket, for the 24h heat pattern."""
    subset = df if flag is None else df.loc[df["Productivity_Flag"] == flag]
    grouped = subset.groupby("Start_Hour")["Duration_Minutes"].sum().reindex(
        range(24), fill_value=0
    ).reset_index()
    grouped.columns = ["Hour", "Total_Minutes"]
    return grouped


def daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Date-wise totals split by productive vs non-productive minutes."""
    grouped = (
        df.groupby(["Date", "Productivity_Flag"])["Duration_Minutes"]
        .sum()
        .reset_index()
    )
    pivot = grouped.pivot(index="Date", columns="Productivity_Flag", values="Duration_Minutes").fillna(0)
    pivot = pivot.reset_index()
    for col in ["Productive", "Non-Productive"]:
        if col not in pivot.columns:
            pivot[col] = 0
    return pivot


def weekday_pattern(df: pd.DataFrame) -> pd.DataFrame:
    """Average non-productive minutes per day-of-week, ordered Mon-Sun."""
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    subset = df.loc[df["Productivity_Flag"] == "Non-Productive"]
    grouped = subset.groupby(["Date", "Day_of_Week"])["Duration_Minutes"].sum().reset_index()
    avg = grouped.groupby("Day_of_Week")["Duration_Minutes"].mean().reindex(order).reset_index()
    avg.columns = ["Day", "Avg_Minutes"]
    avg["Avg_Minutes"] = avg["Avg_Minutes"].fillna(0).round(1)
    return avg


def productivity_ratio(df: pd.DataFrame) -> dict:
    """Overall productive vs non-productive split as percentages."""
    total = df["Duration_Minutes"].sum()
    if total == 0:
        return {"Productive": 0, "Non-Productive": 0}
    by_flag = df.groupby("Productivity_Flag")["Duration_Minutes"].sum()
    return {
        "Productive": round(by_flag.get("Productive", 0) / total * 100, 1),
        "Non-Productive": round(by_flag.get("Non-Productive", 0) / total * 100, 1),
    }


def projected_yearly_loss(df: pd.DataFrame) -> float:
    """
    Estimate yearly hours lost by extrapolating the observed daily
    average of non-productive time across 365 days.
    """
    avg_daily = daily_average_minutes(df, "Non-Productive")
    return round((avg_daily * 365) / 60, 0)


def generate_insight_sentences(df: pd.DataFrame) -> list[str]:
    """
    Build a short list of plain-English, data-driven insight sentences
    to surface on the dashboard (the 'so what' layer above raw charts).
    """
    insights = []

    top_activities = top_time_draining_activities(df, n=1)
    if not top_activities.empty:
        name = top_activities.iloc[0]["Activity_Name"]
        hours = top_activities.iloc[0]["Hours"]
        insights.append(
            f"Your single biggest time drain is **{name}**, consuming roughly "
            f"**{hours} hours** across the logged period."
        )

    cat = category_breakdown(df)
    if not cat.empty:
        top_cat = cat.iloc[0]
        insights.append(
            f"The **{top_cat['Category']}** category alone accounts for "
            f"**{top_cat['Percentage']}%** of all tracked time."
        )

    hourly = hourly_distribution(df, "Non-Productive")
    if hourly["Total_Minutes"].sum() > 0:
        peak_hour = int(hourly.loc[hourly["Total_Minutes"].idxmax(), "Hour"])
        period = "morning" if peak_hour < 12 else "afternoon" if peak_hour < 17 else "evening" if peak_hour < 21 else "night"
        insights.append(
            f"Most invisible time leaks happen around **{peak_hour}:00**, "
            f"during the {period} hours."
        )

    weekday = weekday_pattern(df)
    if weekday["Avg_Minutes"].sum() > 0:
        worst_day = weekday.loc[weekday["Avg_Minutes"].idxmax(), "Day"]
        insights.append(
            f"**{worst_day}** tends to be your most distracted day of the week on average."
        )

    yearly = projected_yearly_loss(df)
    if yearly > 0:
        insights.append(
            f"At your current pace, this projects to roughly **{int(yearly)} hours per year** "
            "lost to invisible, non-productive time — that's over "
            f"**{round(yearly/24, 1)} full days**."
        )

    return insights
