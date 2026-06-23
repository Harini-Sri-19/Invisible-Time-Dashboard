"""
generate_dataset.py
--------------------
One-off utility script used to generate the sample dataset
'invisible_time_data.csv' shipped with this project.

This is NOT required to run the dashboard (the CSV is already
included), but it is kept in the repo so the data generation
logic is transparent and reproducible for academic review.

Run with:  python data/generate_dataset.py
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# Reproducibility
random.seed(42)
np.random.seed(42)

# ----------------------------------------------------------------------
# Activity catalogue: each activity belongs to a category, has a typical
# duration range (in minutes), a productivity flag, and a typical
# "time of day" window it tends to occur in (24h hour range) so the
# generated timestamps feel realistic.
# ----------------------------------------------------------------------
ACTIVITIES = [
    # name, category, min_dur, max_dur, productive, hour_start, hour_end
    ("Social Media Scrolling", "Social Media", 5, 65, "Non-Productive", 7, 23),
    ("Short Video Binge (Reels/Shorts)", "Social Media", 10, 90, "Non-Productive", 12, 24),
    ("Messaging / Chat Apps", "Phone Usage", 3, 40, "Non-Productive", 7, 23),
    ("Random Phone Unlocking", "Phone Usage", 1, 15, "Non-Productive", 6, 24),
    ("Checking Notifications", "Phone Usage", 1, 10, "Non-Productive", 6, 24),
    ("Waiting in Queue (Billing/Counter)", "Waiting", 5, 35, "Non-Productive", 9, 21),
    ("Waiting for Public Transport", "Waiting", 5, 30, "Non-Productive", 7, 22),
    ("Traffic / Commute Delay", "Traffic", 10, 75, "Non-Productive", 7, 21),
    ("Stuck in Traffic Signal Jams", "Traffic", 5, 40, "Non-Productive", 8, 20),
    ("Streaming TV/Web Series", "Entertainment", 20, 120, "Non-Productive", 17, 24),
    ("YouTube Browsing", "Entertainment", 10, 90, "Non-Productive", 10, 24),
    ("Online Gaming", "Entertainment", 15, 120, "Non-Productive", 14, 24),
    ("Overthinking / Indecision", "Decision Fatigue", 5, 45, "Non-Productive", 8, 23),
    ("Choosing What to Eat", "Decision Fatigue", 5, 25, "Non-Productive", 7, 21),
    ("Choosing What to Watch", "Decision Fatigue", 3, 20, "Non-Productive", 18, 23),
    ("Daydreaming / Zoning Out", "Idle Time", 5, 40, "Non-Productive", 8, 22),
    ("Searching for Misplaced Items", "Idle Time", 3, 20, "Non-Productive", 7, 22),
    ("Procrastination Breaks", "Idle Time", 5, 50, "Non-Productive", 9, 22),
    ("Deep Work / Study Session", "Productive Work", 30, 150, "Productive", 8, 22),
    ("Focused Project Work", "Productive Work", 30, 180, "Productive", 9, 21),
    ("Exercise / Workout", "Health", 20, 75, "Productive", 5, 21),
    ("Reading a Book", "Learning", 15, 60, "Productive", 7, 23),
    ("Online Course / Tutorial", "Learning", 20, 90, "Productive", 9, 22),
    ("Meal Preparation / Eating", "Daily Living", 15, 50, "Productive", 7, 22),
    ("Sleep Routine / Wind Down", "Daily Living", 10, 40, "Productive", 21, 24),
]

# Weighted sampling so "invisible" categories appear more frequently
WEIGHTS = [
    14, 10, 9, 8, 7,   # social media + phone usage cluster (heavy)
    6, 5, 7, 5,        # waiting + traffic
    9, 8, 6,           # entertainment
    6, 4, 3,           # decision fatigue
    5, 4, 5,           # idle time
    6, 5,              # productive work
    4, 4, 4,           # health / learning
    5, 3,              # daily living
]

NUM_DAYS = 90          # ~3 months of history
MIN_RECORDS_PER_DAY = 6
MAX_RECORDS_PER_DAY = 14

START_DATE = datetime(2025, 9, 1)


def random_time_in_window(base_date, hour_start, hour_end):
    """Generate a random datetime within a given hour window on base_date."""
    hour_end = min(hour_end, 23)
    hour = random.randint(hour_start, hour_end)
    minute = random.randint(0, 59)
    return base_date.replace(hour=hour, minute=minute, second=0, microsecond=0)


def inject_messiness(value, field_type):
    """
    Occasionally corrupt a value to simulate real-world messy data,
    so the dashboard's cleaning logic has something genuine to do.
    ~3% corruption rate, kept low so analysis remains meaningful.
    """
    if random.random() < 0.015:
        if field_type == "duration":
            return None  # missing duration
        if field_type == "category":
            return ""  # blank category
        if field_type == "flag":
            return None  # missing flag
    return value


def generate_dataset():
    rows = []
    record_id = 1

    for day_offset in range(NUM_DAYS):
        current_date = START_DATE + timedelta(days=day_offset)
        num_records = random.randint(MIN_RECORDS_PER_DAY, MAX_RECORDS_PER_DAY)

        # Track used time slots loosely to avoid too much overlap chaos
        day_activities = random.choices(ACTIVITIES, weights=WEIGHTS, k=num_records)

        for activity in day_activities:
            name, category, min_d, max_d, flag, h_start, h_end = activity

            duration = int(np.clip(np.random.normal((min_d + max_d) / 2, (max_d - min_d) / 4),
                                    min_d, max_d))

            start_dt = random_time_in_window(current_date, h_start, h_end)
            end_dt = start_dt + timedelta(minutes=duration)

            row = {
                "Record_ID": record_id,
                "Date": current_date.strftime("%Y-%m-%d"),
                "Activity_Name": name,
                "Category": inject_messiness(category, "category"),
                "Duration_Minutes": inject_messiness(duration, "duration"),
                "Productivity_Flag": inject_messiness(flag, "flag"),
                "Start_Time": start_dt.strftime("%H:%M"),
                "End_Time": end_dt.strftime("%H:%M"),
            }
            rows.append(row)
            record_id += 1

    df = pd.DataFrame(rows)
    df = df.sort_values(by=["Date", "Start_Time"]).reset_index(drop=True)
    df["Record_ID"] = range(1, len(df) + 1)
    return df


if __name__ == "__main__":
    dataset = generate_dataset()
    output_path = "data/invisible_time_data.csv"
    dataset.to_csv(output_path, index=False)
    print(f"Generated {len(dataset)} records -> {output_path}")
