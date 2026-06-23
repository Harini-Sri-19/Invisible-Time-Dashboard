"""
app.py
-------
Invisible Time Dashboard — main Streamlit entry point.

This app helps users discover how much of their day disappears into
unnoticed, "invisible" activities (social media, phone checks, waiting,
traffic, decision fatigue, idle drifting) versus genuinely productive time.

Run with:
    streamlit run app.py

Author: AI & Data Science Portfolio Project
"""

from datetime import datetime

import pandas as pd
import streamlit as st

from utils.data_loader import get_clean_dataset
from utils.insights import (
    total_hours_lost,
    daily_average_minutes,
    top_time_draining_activities,
    category_breakdown,
    hourly_distribution,
    daily_trend,
    weekday_pattern,
    productivity_ratio,
    projected_yearly_loss,
    generate_insight_sentences,
)
from utils.charts import (
    category_donut,
    top_activities_bar,
    hourly_pattern_area,
    daily_trend_line,
    weekday_radial_bar,
    productivity_gauge,
    category_treemap,
)
from utils.theme import (
    COLORS,
    inject_custom_css,
    render_hero,
    render_metric_card,
    render_section_title,
    render_divider,
)

# ----------------------------------------------------------------------
# Page configuration — must be the first Streamlit call
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Invisible Time Dashboard",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

DATA_PATH = "data/invisible_time_data.csv"

# ----------------------------------------------------------------------
# Load + clean data (cached internally by data_loader)
# ----------------------------------------------------------------------
try:
    df, cleaning_report = get_clean_dataset(DATA_PATH)
except FileNotFoundError as e:
    st.error(str(e))
    st.stop()

if df.empty:
    st.warning(
        "The dataset loaded successfully but contains no usable rows after "
        "cleaning. Please check the CSV file for valid data."
    )
    st.stop()

# ----------------------------------------------------------------------
# Sidebar — filters & data quality panel
# ----------------------------------------------------------------------
with st.sidebar:
    st.markdown("### ◈ Invisible Time")
    st.caption("Where does your day actually go?")
    render_divider()

    st.markdown("**Filter by date range**")
    min_date, max_date = df["Date"].min().date(), df["Date"].max().date()
    date_range = st.date_input(
        "Date range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed",
    )

    st.markdown("**Filter by category**")
    all_categories = sorted(df["Category"].unique().tolist())
    selected_categories = st.multiselect(
        "Categories",
        options=all_categories,
        default=all_categories,
        label_visibility="collapsed",
    )

    render_divider()
    st.markdown("**Data quality report**")
    st.caption(
        f"```\n"
        f"Raw rows:         {cleaning_report['original_rows']}\n"
        f"Duplicates removed: {cleaning_report['duplicate_rows_dropped']}\n"
        f"Categories filled:  {cleaning_report['missing_category_filled']}\n"
        f"Flags inferred:     {cleaning_report['missing_flag_inferred']}\n"
        f"Invalid durations:  {cleaning_report['missing_duration_dropped'] + cleaning_report['invalid_duration_dropped']}\n"
        f"Final usable rows: {cleaning_report['final_rows']}\n"
        f"```"
    )

    render_divider()
    st.caption("Built with Python · Streamlit · Plotly · Pandas")
    st.caption(f"Last refreshed: {datetime.now().strftime('%d %b %Y, %H:%M')}")

# ----------------------------------------------------------------------
# Apply filters
# ----------------------------------------------------------------------
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_d, end_d = date_range
else:
    start_d, end_d = min_date, max_date

mask = (
    (df["Date"].dt.date >= start_d)
    & (df["Date"].dt.date <= end_d)
    & (df["Category"].isin(selected_categories))
)
fdf = df.loc[mask].copy()

if fdf.empty:
    st.warning("No records match the selected filters. Try widening the date range or categories.")
    st.stop()

# ----------------------------------------------------------------------
# Hero section
# ----------------------------------------------------------------------
render_hero(
    title="Discover Where Your Day Disappears",
    subtitle=(
        "Most of us lose hours every day to scrolling, waiting, deciding, and drifting — "
        "without ever noticing. This dashboard turns your activity log into a clear picture "
        "of where invisible time actually goes, so you can take it back."
    ),
)

# ----------------------------------------------------------------------
# Top metric cards
# ----------------------------------------------------------------------
non_prod_hours = total_hours_lost(fdf, "Non-Productive")
prod_hours = total_hours_lost(fdf, "Productive")
avg_daily_lost = daily_average_minutes(fdf, "Non-Productive")
ratio = productivity_ratio(fdf)
yearly_projection = projected_yearly_loss(fdf)

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_metric_card("⏳", "Invisible Time Lost", f"{non_prod_hours} h", COLORS["phantom_violet"],
                        f"across {fdf['Date'].nunique()} logged days")
with col2:
    render_metric_card("✦", "Productive Time", f"{prod_hours} h", COLORS["ghost_cyan"],
                        f"{ratio['Productive']}% of total")
with col3:
    render_metric_card("◷", "Avg. Lost / Day", f"{avg_daily_lost:.0f} min", COLORS["drift_blue"],
                        "non-productive average")
with col4:
    render_metric_card("⚠", "Yearly Projection", f"{int(yearly_projection)} h", COLORS["rose_alert"],
                        f"≈ {round(yearly_projection/24,1)} days/year")

render_divider()

# ----------------------------------------------------------------------
# Insight sentences (the "so what" layer)
# ----------------------------------------------------------------------
render_section_title("◆", "Key Insights", "Plain-language takeaways generated directly from your data")
insight_list = generate_insight_sentences(fdf)
insight_cols = st.columns(2)
for i, sentence in enumerate(insight_list):
    with insight_cols[i % 2]:
        st.markdown(f'<div class="insight-card">{sentence}</div>', unsafe_allow_html=True)

render_divider()

# ----------------------------------------------------------------------
# Tabbed analysis sections
# ----------------------------------------------------------------------
tab_overview, tab_patterns, tab_trends, tab_data = st.tabs(
    ["◈ Overview", "◷ Time Patterns", "↗ Trends", "▤ Raw Data"]
)

with tab_overview:
    col_a, col_b = st.columns([1, 1])

    with col_a:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        render_section_title("◆", "Time Split by Category")
        cat_df = category_breakdown(fdf)
        st.plotly_chart(category_donut(cat_df), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        render_section_title("▥", "Top Time-Draining Activities")
        top_df = top_time_draining_activities(fdf, n=6)
        if not top_df.empty:
            st.plotly_chart(top_activities_bar(top_df), use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("No non-productive activities found in the selected filters.")
        st.markdown('</div>', unsafe_allow_html=True)

    col_c, col_d = st.columns([1, 1])
    with col_c:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        render_section_title("▦", "Category Density Map")
        st.plotly_chart(category_treemap(cat_df), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
        render_section_title("◎", "Overall Productivity Score")
        st.plotly_chart(productivity_gauge(ratio), use_container_width=True, config={"displayModeBar": False})
        st.caption(
            f"Productive: {ratio['Productive']}%  ·  Non-Productive: {ratio['Non-Productive']}%"
        )
        st.markdown('</div>', unsafe_allow_html=True)

with tab_patterns:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    render_section_title("◷", "24-Hour Invisible Time Pattern", "When during the day does time slip away the most?")
    hourly_df = hourly_distribution(fdf, "Non-Productive")
    st.plotly_chart(hourly_pattern_area(hourly_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    render_section_title("▤", "Weekday Pattern", "Average minutes lost per day of the week")
    weekday_df = weekday_pattern(fdf)
    st.plotly_chart(weekday_radial_bar(weekday_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with tab_trends:
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    render_section_title("↗", "Productive vs Non-Productive Over Time")
    trend_df = daily_trend(fdf)
    st.plotly_chart(daily_trend_line(trend_df), use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Category trend explorer
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    render_section_title("◈", "Explore a Single Category Over Time")
    chosen_cat = st.selectbox("Choose a category", options=sorted(fdf["Category"].unique()))
    cat_subset = fdf.loc[fdf["Category"] == chosen_cat]
    cat_daily = cat_subset.groupby("Date")["Duration_Minutes"].sum().reset_index()
    if not cat_daily.empty:
        import plotly.graph_objects as go
        fig = go.Figure(
            data=[
                go.Bar(
                    x=cat_daily["Date"], y=cat_daily["Duration_Minutes"],
                    marker=dict(color=COLORS["phantom_violet"]),
                    hovertemplate="%{x|%b %d}<br>%{y:.0f} min<extra></extra>",
                )
            ]
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=COLORS["text_primary"]), height=300,
            margin=dict(l=10, r=10, t=10, b=10), showlegend=False,
        )
        fig.update_xaxes(showgrid=False, color=COLORS["text_secondary"])
        fig.update_yaxes(showgrid=True, gridcolor=COLORS["grid_line"], color=COLORS["text_secondary"])
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with tab_data:
    render_section_title("▤", "Cleaned Dataset", f"{len(fdf)} records after filtering and cleaning")
    st.dataframe(
        fdf[
            [
                "Record_ID", "Date", "Activity_Name", "Category",
                "Duration_Minutes", "Productivity_Flag", "Start_Time", "End_Time",
            ]
        ].sort_values("Date", ascending=False),
        use_container_width=True,
        height=420,
    )

    csv_bytes = fdf.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇ Download filtered data as CSV",
        data=csv_bytes,
        file_name="invisible_time_filtered.csv",
        mime="text/csv",
    )

# ----------------------------------------------------------------------
# Footer
# ----------------------------------------------------------------------
render_divider()
st.markdown(
    f"""
    <div style="text-align:center; color:{COLORS['text_secondary']}; font-size:0.82rem; padding-bottom:1rem;">
        Invisible Time Dashboard · Built with Streamlit, Pandas &amp; Plotly ·
        A data science portfolio project exploring everyday attention loss
    </div>
    """,
    unsafe_allow_html=True,
)
