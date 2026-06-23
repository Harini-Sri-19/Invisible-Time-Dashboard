"""
theme.py
---------
Centralised visual identity for the Invisible Time Dashboard.

Design concept: "time dissolving into a void." The dark background
represents the unnoticed hours that slip away; cyan represents
intentional/productive time that stays "visible"; violet represents
invisible, drifting, non-productive time. A drifting particle field
in the hero section visualises hours evaporating.

This module exposes:
    - COLORS: a dict of named hex tokens used consistently across
      both the custom CSS and the Plotly chart palettes in app.py.
    - inject_custom_css(): writes the full CSS block into the page.
    - render_hero(): renders the animated hero banner.
"""

import streamlit as st

# ----------------------------------------------------------------------
# Design tokens — single source of truth for color across CSS + Plotly
# ----------------------------------------------------------------------
COLORS = {
    "void": "#0A0E16",            # page background — the "void" time vanishes into
    "surface": "#121826",         # card surfaces
    "surface_alt": "#161E30",     # slightly raised surface (hover/active)
    "border": "#232C42",          # hairline borders on cards
    "text_primary": "#E7EAF2",    # primary readable text
    "text_secondary": "#8A93A8",  # muted captions / labels
    "ghost_cyan": "#5EEAD4",      # productive / visible time
    "phantom_violet": "#A78BFA", # non-productive / invisible time
    "drift_blue": "#60A5FA",      # secondary accent (waiting/traffic)
    "amber_warn": "#FBBF24",      # attention / warning accent
    "rose_alert": "#FB7185",      # high-loss alert accent
    "grid_line": "#1C2436",       # chart gridlines
}

# Ordered categorical palette for charts with many categories
CATEGORY_PALETTE = [
    "#A78BFA",  # Social Media
    "#60A5FA",  # Phone Usage
    "#FB7185",  # Waiting
    "#FBBF24",  # Traffic
    "#F472B6",  # Entertainment
    "#FB923C",  # Decision Fatigue
    "#818CF8",  # Idle Time
    "#5EEAD4",  # Productive Work
    "#34D399",  # Health
    "#22D3EE",  # Learning
    "#A3E635",  # Daily Living
    "#64748B",  # Uncategorized
]


def inject_custom_css():
    """Inject the full custom CSS theme into the Streamlit page."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* ---------- Base page ---------- */
        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 15% 0%, rgba(167,139,250,0.07), transparent 40%),
                radial-gradient(circle at 85% 10%, rgba(94,234,212,0.06), transparent 40%),
                {COLORS['void']};
            color: {COLORS['text_primary']};
        }}

        /* Hide default Streamlit chrome for a cleaner premium feel */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        section[data-testid="stSidebar"] {{
            background: {COLORS['surface']};
            border-right: 1px solid {COLORS['border']};
        }}

        section[data-testid="stSidebar"] * {{
            color: {COLORS['text_primary']};
        }}

        /* ---------- Typography ---------- */
        h1, h2, h3 {{
            font-family: 'Space Grotesk', sans-serif !important;
            letter-spacing: -0.01em;
        }}

        .eyebrow {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            color: {COLORS['phantom_violet']};
            opacity: 0.85;
        }}

        /* ---------- Hero ---------- */
        .hero-wrap {{
            position: relative;
            border-radius: 18px;
            padding: 2.6rem 2.4rem;
            margin-bottom: 1.6rem;
            background: linear-gradient(135deg, {COLORS['surface']} 0%, #0E1422 100%);
            border: 1px solid {COLORS['border']};
            overflow: hidden;
        }}

        .hero-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 2.4rem;
            font-weight: 700;
            line-height: 1.15;
            margin: 0.3rem 0 0.6rem 0;
            background: linear-gradient(90deg, {COLORS['text_primary']} 40%, {COLORS['phantom_violet']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-sub {{
            color: {COLORS['text_secondary']};
            font-size: 1.0rem;
            max-width: 640px;
            line-height: 1.55;
        }}

        .particle {{
            position: absolute;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(167,139,250,0.9), rgba(167,139,250,0));
            animation: drift 14s linear infinite;
            opacity: 0.55;
        }}

        @keyframes drift {{
            0%   {{ transform: translateY(0) translateX(0) scale(1); opacity: 0.6; }}
            50%  {{ transform: translateY(-40px) translateX(10px) scale(1.15); opacity: 0.25; }}
            100% {{ transform: translateY(-90px) translateX(-6px) scale(0.6); opacity: 0; }}
        }}

        /* ---------- Metric cards ---------- */
        .metric-card {{
            background: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-left: 3px solid var(--accent, {COLORS['ghost_cyan']});
            border-radius: 14px;
            padding: 1.15rem 1.3rem;
            transition: transform 0.18s ease, border-color 0.18s ease;
            height: 100%;
        }}

        .metric-card:hover {{
            transform: translateY(-3px);
            border-color: var(--accent, {COLORS['ghost_cyan']});
        }}

        .metric-icon {{
            font-size: 1.3rem;
            opacity: 0.9;
        }}

        .metric-label {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: {COLORS['text_secondary']};
            margin-top: 0.5rem;
        }}

        .metric-value {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.9rem;
            font-weight: 700;
            color: {COLORS['text_primary']};
            margin-top: 0.15rem;
        }}

        .metric-delta {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.78rem;
            margin-top: 0.3rem;
        }}

        /* ---------- Section headers ---------- */
        .section-title {{
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: {COLORS['text_primary']};
            margin: 0.4rem 0 0.1rem 0;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}

        .section-caption {{
            color: {COLORS['text_secondary']};
            font-size: 0.86rem;
            margin-bottom: 1.0rem;
        }}

        /* ---------- Insight cards ---------- */
        .insight-card {{
            background: {COLORS['surface_alt']};
            border: 1px solid {COLORS['border']};
            border-radius: 12px;
            padding: 0.95rem 1.15rem;
            margin-bottom: 0.65rem;
            font-size: 0.92rem;
            line-height: 1.55;
            color: {COLORS['text_primary']};
            border-left: 3px solid {COLORS['phantom_violet']};
        }}

        .insight-card b {{
            color: {COLORS['ghost_cyan']};
        }}

        /* ---------- Generic card wrapper for chart panels ---------- */
        .chart-panel {{
            background: {COLORS['surface']};
            border: 1px solid {COLORS['border']};
            border-radius: 16px;
            padding: 1.3rem 1.4rem 0.6rem 1.4rem;
            margin-bottom: 1.3rem;
        }}

        /* ---------- Divider ---------- */
        .ghost-divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent, {COLORS['border']}, transparent);
            margin: 1.6rem 0;
        }}

        /* ---------- Tag pill ---------- */
        .tag-pill {{
            display: inline-block;
            background: rgba(167,139,250,0.12);
            color: {COLORS['phantom_violet']};
            border: 1px solid rgba(167,139,250,0.35);
            border-radius: 999px;
            padding: 0.2rem 0.7rem;
            font-size: 0.72rem;
            font-family: 'JetBrains Mono', monospace;
            letter-spacing: 0.04em;
        }}

        /* Streamlit dataframe dark tuning */
        [data-testid="stDataFrame"] {{
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid {COLORS['border']};
        }}

        /* Tabs */
        button[data-baseweb="tab"] {{
            font-family: 'Space Grotesk', sans-serif;
            color: {COLORS['text_secondary']};
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {COLORS['ghost_cyan']} !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str, eyebrow: str = "INVISIBLE TIME · ANALYTICS"):
    """Render the animated hero banner with drifting 'time particles'."""
    particles_html = "".join(
        f"""<div class="particle" style="
                width:{6 + (i % 4) * 4}px; height:{6 + (i % 4) * 4}px;
                left:{(i * 8.7) % 95}%; bottom:{(i * 11) % 60}%;
                animation-delay:{i * 0.9}s;"></div>"""
        for i in range(16)
    )

    st.markdown(
        f"""
        <div class="hero-wrap">
            {particles_html}
            <div class="eyebrow">{eyebrow}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(icon: str, label: str, value: str, accent: str, delta: str = ""):
    """Render a single custom-styled metric card (used instead of st.metric for full styling control)."""
    delta_html = f'<div class="metric-delta" style="color:{accent};">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="metric-card" style="--accent:{accent};">
            <div class="metric-icon">{icon}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_title(icon: str, title: str, caption: str = ""):
    """Render a consistent section header used above each chart panel."""
    st.markdown(f'<div class="section-title">{icon} {title}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="section-caption">{caption}</div>', unsafe_allow_html=True)


def render_divider():
    st.markdown('<div class="ghost-divider"></div>', unsafe_allow_html=True)
