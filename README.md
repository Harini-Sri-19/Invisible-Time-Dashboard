# ◈ Invisible Time Dashboard

> *Most of us lose hours every day to scrolling, waiting, deciding, and drifting — without ever noticing. This dashboard turns a simple activity log into a clear, visual picture of where your time actually goes.*

A premium, dark-themed analytics dashboard built with **Python + Streamlit** that analyzes how people unknowingly spend their time on hidden, low-awareness activities — social media scrolling, phone checking, waiting in queues, traffic, entertainment binges, decision fatigue, and idle drifting — versus genuinely productive time.

Built as an **AI & Data Science portfolio project**, demonstrating data cleaning, exploratory analysis, insight generation, and modern dashboard UI design.

---

## ✦ Project Overview

We rarely notice where small chunks of time go: five minutes checking notifications here, twenty minutes in traffic there, an hour of "just one more video." Individually these feel harmless. Added up over a year, they can total weeks of lost time.

**Invisible Time Dashboard** ingests a day-by-day activity log (date, activity, category, duration, productive/non-productive flag, start/end time) and turns it into:

- Clear headline metrics (total hours lost, productivity ratio, yearly projection)
- Visual breakdowns by category and activity
- Time-of-day and day-of-week behavioral patterns
- Plain-language, auto-generated insights
- A filterable, downloadable data explorer

---

## ✦ Features

| Area | Details |
|---|---|
| **Modern dark UI** | Custom CSS theme — deep void background, glassmorphic cards, glowing accent borders, animated drifting-particle hero banner |
| **Key metrics** | Invisible time lost, productive time, average daily loss, projected yearly loss |
| **Auto-generated insights** | Plain-English sentences computed live from the filtered dataset (top time drain, peak hour, worst weekday, yearly projection) |
| **Category breakdown** | Interactive donut chart + treemap of time-by-category |
| **Top time drains** | Horizontal ranked bar chart of the biggest non-productive activities |
| **24-hour pattern** | Area chart showing when during the day time most often slips away |
| **Weekday pattern** | Bar chart highlighting the most distracted day of the week |
| **Trend analysis** | Productive vs. non-productive minutes over time, plus a per-category explorer |
| **Data quality panel** | Live sidebar report showing exactly what was cleaned (missing values filled, duplicates removed, invalid rows dropped) |
| **Filters** | Date range and category multi-select, applied across the entire dashboard |
| **Data export** | Download the filtered, cleaned dataset as CSV directly from the app |

---

## ✦ Project Structure

```
invisible-time-dashboard/
│
├── app.py                      # Main Streamlit application (entry point)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
│
├── .streamlit/
│   └── config.toml             # Streamlit dark theme + server configuration
│
├── data/
│   ├── invisible_time_data.csv # Sample dataset (~900 records, 90 days)
│   └── generate_dataset.py     # Script used to generate the sample dataset
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py          # CSV loading, validation, and cleaning logic
│   ├── insights.py             # Metric calculations + auto-generated insights
│   ├── charts.py                # Themed Plotly chart builders
│   └── theme.py                 # Custom CSS theme + reusable UI components
│
└── assets/                     # Reserved for screenshots / static assets
```

---

## ✦ Installation & Setup

### Prerequisites
- Python 3.9 or higher
- pip (Python package manager)

### Steps

1. **Extract / clone the project** and open the folder in VS Code (or your terminal of choice). No restructuring is needed — it runs as-is.

2. **(Recommended) Create a virtual environment**

   ```bash
   python -m venv venv
   ```

   Activate it:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the dashboard**

   ```bash
   streamlit run app.py
   ```

5. Streamlit will automatically open the dashboard in your default browser at:

   ```
   http://localhost:8501
   ```

   If it doesn't open automatically, copy that URL into your browser manually.

---

## ✦ Required Libraries

All pinned in `requirements.txt`:

- **streamlit** — dashboard frontend / web app framework
- **pandas** — data loading, cleaning, and aggregation
- **numpy** — numerical operations used during data generation/cleaning
- **plotly** — primary interactive visualizations (donut, bar, area, treemap, gauge)
- **matplotlib** / **seaborn** — included for optional/extended static visualizations and available for further analysis

---

## ✦ Dataset Explanation

The included sample dataset, `data/invisible_time_data.csv`, contains **~900 synthetic but realistic records spanning 90 days** (Sept – Nov 2025), generated by `data/generate_dataset.py` using weighted random sampling so common "invisible" activities (social media, phone checks, entertainment) appear more frequently than occasional ones — mirroring real behavioral patterns.

### Columns

| Column | Description |
|---|---|
| `Record_ID` | Unique identifier for each logged activity |
| `Date` | Calendar date of the activity (YYYY-MM-DD) |
| `Activity_Name` | Specific activity, e.g. "Social Media Scrolling", "Waiting in Queue" |
| `Category` | Higher-level grouping, e.g. Social Media, Traffic, Decision Fatigue, Productive Work |
| `Duration_Minutes` | How long the activity lasted, in minutes |
| `Productivity_Flag` | `Productive` or `Non-Productive` |
| `Start_Time` | Activity start time (HH:MM, 24-hour) |
| `End_Time` | Activity end time (HH:MM, 24-hour) |

### Intentional data messiness

To demonstrate real-world data cleaning (a core requirement of this project), the generator deliberately injects a small amount of realistic messiness:
- ~1–2% missing `Category` values → cleaned to `"Uncategorized"`
- ~1–2% missing `Duration_Minutes` values → removed with a logged count
- ~1–2% missing `Productivity_Flag` values → inferred from category, with a logged count

The sidebar **Data Quality Report** shows exactly how many rows were affected and how each issue was resolved, every time the app runs.

### Using your own data

Replace `data/invisible_time_data.csv` with your own file using the same column headers, or point `DATA_PATH` in `app.py` to a different file. The cleaning pipeline in `utils/data_loader.py` will handle missing/invalid values automatically.

---

## ✦ Screenshots

> *Add screenshots after first run — recommended views below.*

| View | Screenshot |
|---|---|
| Hero + key metrics | `assets/screenshot_hero.png` |
| Overview tab (donut + top activities) | `assets/screenshot_overview.png` |
| Time patterns tab | `assets/screenshot_patterns.png` |
| Trends tab | `assets/screenshot_trends.png` |
| Raw data explorer | `assets/screenshot_data.png` |

---

## ✦ Design Notes

The visual identity is built around a single idea: **time dissolving into a void**.

- **Background**: a near-black "void" (`#0A0E16`) that the hours quietly vanish into
- **Phantom violet** (`#A78BFA`): represents invisible / non-productive time
- **Ghost cyan** (`#5EEAD4`): represents visible / productive time
- **Hero banner**: animated drifting particles evoke minutes evaporating
- **Typography**: Space Grotesk (display) + Inter (body) + JetBrains Mono (data/labels), for a precise, instrument-like analytics feel
- **Cards**: glassmorphic surfaces with glowing left-border accents, subtle hover lift

All design tokens live in one place — `utils/theme.py` — for easy customization.

---

## ✦ Future Enhancements

- [ ] User authentication and multi-user data storage
- [ ] Manual activity logging form directly inside the dashboard
- [ ] Integration with phone screen-time exports (iOS/Android) for real data
- [ ] Goal-setting and weekly progress tracking against a target
- [ ] Predictive modeling (ML) to forecast future time-loss trends
- [ ] Smart notifications/nudges when a non-productive pattern is detected
- [ ] PDF/weekly email report export
- [ ] Comparative analytics (this week vs last week, this month vs last month)
- [ ] Mobile-responsive layout refinements

---

## ✦ Tech Stack Summary

- **Language**: Python 3.9+
- **Frontend / Dashboard**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly (primary), Matplotlib, Seaborn
- **Styling**: Custom CSS injected via Streamlit, Google Fonts (Space Grotesk, Inter, JetBrains Mono)

No external web frameworks (Flask/Django) are used — this is a pure Python + Streamlit application.

---

## ✦ License & Use

This project was created as an academic/portfolio demonstration for AI & Data Science coursework and project reviews. Free to use, modify, and extend for learning purposes.

---

*Built to make the invisible, visible.*
