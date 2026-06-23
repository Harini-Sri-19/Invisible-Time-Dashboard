"""
data_loader.py
----------------
Handles loading, validating, and cleaning the Invisible Time dataset.

Keeping this logic separate from app.py keeps the Streamlit file focused
purely on presentation, while this module owns data integrity.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

# Canonical category list used for validation and consistent ordering
# across every chart in the dashboard.
VALID_CATEGORIES = [
    "Social Media",
    "Phone Usage",
    "Waiting",
    "Traffic",
    "Entertainment",
    "Decision Fatigue",
    "Idle Time",
    "Productive Work",
    "Health",
    "Learning",
    "Daily Living",
]

VALID_FLAGS = ["Productive", "Non-Productive"]


@st.cache_data(show_spinner=False)
def load_raw_data(csv_path: str) -> pd.DataFrame:
    """
    Load the raw CSV from disk. Cached so repeated Streamlit reruns
    (e.g. on every widget interaction) don't re-read the file from disk.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Dataset not found at '{csv_path}'. "
            "Make sure 'invisible_time_data.csv' exists inside the data/ folder."
        )
    df = pd.read_csv(path)
    return df


def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Clean and validate the raw dataframe, handling missing values and
    invalid entries gracefully rather than crashing the app.

    Returns the cleaned dataframe plus a small report dict describing
    what was fixed, so the UI can be transparent about data quality.
    """
    report = {
        "original_rows": len(df),
        "missing_category_filled": 0,
        "missing_duration_dropped": 0,
        "missing_flag_inferred": 0,
        "invalid_duration_dropped": 0,
        "duplicate_rows_dropped": 0,
    }

    df = df.copy()

    # --- Drop exact duplicate records ---------------------------------
    before = len(df)
    df = df.drop_duplicates()
    report["duplicate_rows_dropped"] = before - len(df)

    # --- Normalise text columns ----------------------------------------
    for col in ["Activity_Name", "Category", "Productivity_Flag"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace({"nan": pd.NA, "": pd.NA, "None": pd.NA})

    # --- Fix missing Category: infer "Uncategorized" rather than drop --
    if "Category" in df.columns:
        missing_cat_mask = df["Category"].isna()
        report["missing_category_filled"] = int(missing_cat_mask.sum())
        df.loc[missing_cat_mask, "Category"] = "Uncategorized"

    # --- Handle Duration: coerce to numeric, drop rows that are
    #     genuinely unusable (missing or non-positive duration) ---------
    if "Duration_Minutes" in df.columns:
        df["Duration_Minutes"] = pd.to_numeric(df["Duration_Minutes"], errors="coerce")

        invalid_mask = df["Duration_Minutes"].le(0) | df["Duration_Minutes"].isna()
        report["missing_duration_dropped"] = int(df["Duration_Minutes"].isna().sum())
        report["invalid_duration_dropped"] = int((df["Duration_Minutes"].le(0)).sum())

        df = df.loc[~invalid_mask].copy()

        # Cap unrealistic outliers (> 8 hours for a single logged activity)
        df = df.loc[df["Duration_Minutes"] <= 480].copy()

    # --- Infer missing Productivity_Flag from category where possible --
    if "Productivity_Flag" in df.columns and "Category" in df.columns:
        productive_categories = {"Productive Work", "Health", "Learning", "Daily Living"}
        missing_flag_mask = df["Productivity_Flag"].isna()
        report["missing_flag_inferred"] = int(missing_flag_mask.sum())

        inferred = df.loc[missing_flag_mask, "Category"].apply(
            lambda c: "Productive" if c in productive_categories else "Non-Productive"
        )
        df.loc[missing_flag_mask, "Productivity_Flag"] = inferred

        # Final safety net: anything still invalid defaults to Non-Productive
        df["Productivity_Flag"] = df["Productivity_Flag"].where(
            df["Productivity_Flag"].isin(VALID_FLAGS), "Non-Productive"
        )

    # --- Parse Date column -----------------------------------------------
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        df = df.dropna(subset=["Date"])

    # --- Parse Start/End time into proper time-of-day + derived hour ----
    for col in ["Start_Time", "End_Time"]:
        if col in df.columns:
            parsed = pd.to_datetime(df[col], format="%H:%M", errors="coerce")
            df[col + "_parsed"] = parsed.dt.time

    if "Start_Time_parsed" in df.columns:
        df["Start_Hour"] = pd.to_datetime(
            df["Start_Time"], format="%H:%M", errors="coerce"
        ).dt.hour

    # --- Derived helper columns used across multiple charts -------------
    df["Day_of_Week"] = df["Date"].dt.day_name()
    df["Week_Number"] = df["Date"].dt.isocalendar().week
    df["Month"] = df["Date"].dt.strftime("%b %Y")

    report["final_rows"] = len(df)
    return df.reset_index(drop=True), report


def get_clean_dataset(csv_path: str) -> tuple[pd.DataFrame, dict]:
    """Convenience wrapper: load + clean in one call."""
    raw = load_raw_data(csv_path)
    cleaned, report = clean_data(raw)
    return cleaned, report
