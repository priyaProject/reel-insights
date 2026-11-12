import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# REEL INSIGHTS - STREAMLIT ANALYTICS DASHBOARD
# =========================================================

st.set_page_config(
    page_title="Reel Insights",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "reel_insights.db"  # change if your file name differs

# ------------------------- THEME -------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Font is applied to text elements only, so Streamlit icons keep working */
    html, body, .stApp, p, label, h1, h2, h3, h4, input, textarea {
        font-family: 'Inter', sans-serif;
    }

    .stApp { background: #F4F6FA; color: #253247; font-size: 14px; }

    .block-container { max-width: 100% !important; padding: 3.6rem 2rem 1rem 2rem !important; }

    h1 { font-size: 24px !important; font-weight: 700 !important; }
    h2 { font-size: 19px !important; font-weight: 650 !important; }
    h3 { font-size: 16px !important; font-weight: 600 !important; }
    h4 { font-size: 15px !important; font-weight: 600 !important; }
    p, label { font-size: 14px; }
    .stCaption, [data-testid="stCaptionContainer"] { font-size: 12.5px !important; }

    /* Sidebar: fixed width only while expanded, so collapsing leaves no gap */
    section[data-testid="stSidebar"] { background: #18243A; }
    section[data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 270px; max-width: 270px;
    }
    /* Fit everything in one screen: no inner scrollbar on normal laptop heights */
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        overflow-y: hidden !important;
    }
    @media (max-height: 720px) {
        section[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            overflow-y: auto !important;   /* tiny screens: allow scroll so nothing is cut off */
        }
    }
    [data-testid="stSidebarHeader"] {
        height: 1.8rem !important; min-height: 0 !important;
        padding: 0.3rem 0.8rem 0 !important; margin: 0 !important;
    }
    [data-testid="stSidebarUserContent"] { padding: 0.2rem 0.8rem 0.5rem !important; }
    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0.55rem !important; }
    section[data-testid="stSidebar"] [data-testid="stSlider"] { padding-bottom: 0 !important; }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label { padding: 0 !important; }
    section[data-testid="stSidebar"] .stButton button { padding: 0.2rem 0.6rem !important; min-height: 2rem; }
    .sb-label {
        display: block; font-size: 11px; font-weight: 700; letter-spacing: 0.08em;
        line-height: 1.4; color: #8FA3C0;
        margin: 6px 0 10px 0; padding: 0;
    }
    .sb-gap { margin-top: 14px; padding-top: 12px; border-top: 1px solid #2E3E58; }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] { overflow: visible; }

    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #F4F7FB !important;
    }
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #D8E1EE !important; font-size: 13px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background: #FFFFFF !important; border-radius: 7px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] * { color: #253247 !important; }
    [data-testid="stSidebar"] [data-baseweb="select"] svg {
        fill: #42536A !important; color: #42536A !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] { background: #E8EEF7 !important; }
    [data-testid="stSidebar"] [data-baseweb="tag"] span,
    [data-testid="stSidebar"] [data-baseweb="tag"] svg {
        color: #253247 !important; fill: #253247 !important;
    }
    [data-testid="stSidebar"] input { color: #253247 !important; }
    [data-testid="stSidebar"] .stButton button {
        background: #34445E !important; color: #FFFFFF !important;
        border: 1px solid #52627B !important; border-radius: 7px !important;
    }
    [data-testid="stSidebar"] .stButton button:hover { background: #465B7B !important; }

    /* Page title banner: dark gradient so it reads as a header, not content */
    .page-header {
        display: flex; align-items: center; gap: 14px;
        background: #E6EBF3;
        border: 1px solid #D5DCE8;
        border-left: 5px solid #5B7399;
        border-radius: 10px;
        padding: 14px 22px;
        margin: 0 0 16px 0;
        box-shadow: none;
    }
    .page-header .ph-icon {
        font-size: 28px; line-height: 1;
        background: #FFFFFF; border: 1px solid #D5DCE8;
        border-radius: 10px; padding: 7px 9px;
    }
    .page-header h1 {
        margin: 0 !important; padding: 0 !important;
        color: #1E2B42 !important; font-size: 25px !important;
        font-weight: 700 !important; letter-spacing: 0.2px;
    }
    .page-header p { margin: 3px 0 0; color: #5A6B84 !important; font-size: 13.5px !important; }

    [data-testid="stMetric"] {
        background: #FFFFFF; border: 1px solid #E4E9F1; border-radius: 9px;
        padding: 10px 14px; box-shadow: 0 1px 3px rgba(20, 35, 60, 0.04);
    }
    [data-testid="stMetricLabel"] { color: #64748B !important; font-size: 12.5px !important; }
    [data-testid="stMetricValue"] {
        color: #18243A !important; font-size: 24px !important; font-weight: 650 !important;
    }
    [data-testid="stDataFrame"] {
        border: 1px solid #E3E8F0; border-radius: 8px; overflow: hidden;
    }
    [data-testid="stAlert"] { border-radius: 8px; }
    [data-testid="stExpander"] {
        background: #FFFFFF; border: 1px solid #E3E8F0; border-radius: 8px;
    }
    hr { border-color: #E3E8F0; margin: 0.55rem 0; }

    /* ---------- Loader ---------- */
    .rl-loader {
        position: fixed; inset: 0; z-index: 9999;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        gap: 12px; background: rgba(244, 246, 250, 0.72);
        pointer-events: none;
    }
    .rl-spinner {
        width: 46px; height: 46px; border-radius: 50%;
        border: 5px solid #D5DCE8; border-top-color: #3F6AA8;
        animation: rl-spin 0.8s linear infinite;
    }
    .rl-text { color: #42536A; font-size: 14px; font-weight: 600; }
    @keyframes rl-spin { to { transform: rotate(360deg); } }

    /* ---------- Responsive ---------- */
    @media (max-width: 992px) {
        .block-container { padding: 3.2rem 1rem 1rem 1rem !important; }
    }
    @media (max-width: 768px) {
        section[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            overflow-y: auto !important;
        }
    }
    @media (max-width: 640px) {
        .block-container { padding: 3rem 0.6rem 1rem 0.6rem !important; }
        .page-header { padding: 10px 12px; gap: 10px; }
        .page-header h1 { font-size: 19px !important; }
        .page-header .ph-icon { font-size: 20px; padding: 5px 7px; }
        .page-header p { font-size: 12px !important; }
        [data-testid="stMetricValue"] { font-size: 20px !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ------------------------- DATA LOADING -------------------------

@st.cache_data(show_spinner="Loading movie database...")
def load_data(db_path: str):
    if not Path(db_path).exists():
        raise FileNotFoundError(
            f"Database not found: {db_path}. Place reel_insights.db in the "
            "same folder as app.py or update DB_PATH."
        )

    with sqlite3.connect(db_path) as conn:
        tables = {
            r[0]
            for r in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        missing = {"movies", "genres", "movie_genres"} - tables
        if missing:
            raise ValueError("Missing database table(s): " + ", ".join(sorted(missing)))

        movies_df = pd.read_sql_query('SELECT * FROM "movies"', conn)
        genres_df = pd.read_sql_query('SELECT * FROM "genres"', conn)
        mg_df = pd.read_sql_query('SELECT * FROM "movie_genres"', conn)
        if "cast" in tables:
            cast_df = pd.read_sql_query('SELECT * FROM "cast"', conn)
        else:
            cast_df = pd.DataFrame(columns=["movie_id", "person_id", "actor_name"])

    return movies_df, genres_df, mg_df, cast_df


def first_existing(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


try:
    movies, genres, movie_genres, cast = load_data(str(DB_PATH))
except Exception as exc:
    st.error(f"Could not load the database: {exc}")
    st.info(
        "Check that reel_insights.db is in the same folder as app.py "
        "and that its table/column names match your project."
    )
    st.stop()

# Column detection (supports common naming variations)
MOVIE_ID = first_existing(movies, ["movie_id", "id"])
TITLE = first_existing(movies, ["title", "movie_title", "name"])
YEAR = first_existing(movies, ["release_year", "year"])
RELEASE_DATE = first_existing(movies, ["release_date"])
LANGUAGE = first_existing(movies, ["original_language", "language", "original_lang"])
RATING = first_existing(movies, ["vote_average", "rating", "average_rating"])
VOTES = first_existing(movies, ["vote_count", "votes"])
POPULARITY = first_existing(movies, ["popularity"])
BUDGET = first_existing(movies, ["budget_clean", "budget", "budget_adj"])
REVENUE = first_existing(movies, ["revenue_clean", "revenue", "revenue_adj"])

GENRE_ID = first_existing(genres, ["genre_id", "id"])
GENRE_NAME = first_existing(genres, ["genre_name", "name"])
MG_MOVIE_ID = first_existing(movie_genres, ["movie_id"])
MG_GENRE_ID = first_existing(movie_genres, ["genre_id"])

CAST_MOVIE_ID = first_existing(cast, ["movie_id"])
PERSON_ID = first_existing(cast, ["person_id", "cast_id", "actor_id"])
ACTOR_NAME = first_existing(cast, ["actor_name", "name", "person_name"])
HAS_CAST = bool(CAST_MOVIE_ID and PERSON_ID and ACTOR_NAME and not cast.empty)

if any(c is None for c in [MOVIE_ID, TITLE, RATING]):
    st.error(
        "The movies table must contain movie_id, title and vote_average "
        "(or supported equivalent column names)."
    )
    st.write("Available movie columns:", list(movies.columns))
    st.stop()

if not all([GENRE_ID, GENRE_NAME, MG_MOVIE_ID, MG_GENRE_ID]):
    st.error(
        "The genres and movie_genres tables must contain genre_id, "
        "genre_name and movie_id."
    )
    st.write("Genres columns:", list(genres.columns))
    st.write("Movie genres columns:", list(movie_genres.columns))
    st.stop()

# Normalize (copies, so source tables stay untouched)
movies, genres = movies.copy(), genres.copy()
movie_genres, cast = movie_genres.copy(), cast.copy()

for col in [RATING, VOTES, POPULARITY, BUDGET, REVENUE]:
    if col:
        movies[col] = pd.to_numeric(movies[col], errors="coerce")

if YEAR:
    movies[YEAR] = pd.to_numeric(movies[YEAR], errors="coerce")
elif RELEASE_DATE:
    movies["__release_year"] = pd.to_datetime(
        movies[RELEASE_DATE], errors="coerce"
    ).dt.year
    YEAR = "__release_year"
else:
    movies["__release_year"] = pd.NA
    movies["__release_year"] = pd.to_numeric(movies["__release_year"], errors="coerce")
    YEAR = "__release_year"

HAS_YEAR = bool(movies[YEAR].notna().any())

genres[GENRE_NAME] = genres[GENRE_NAME].astype(str)
genre_lookup = genres[[GENRE_ID, GENRE_NAME]].drop_duplicates()

movie_genre_data = movie_genres.merge(
    genre_lookup, left_on=MG_GENRE_ID, right_on=GENRE_ID, how="left"
).dropna(subset=[GENRE_NAME])

if HAS_CAST:
    cast[ACTOR_NAME] = cast[ACTOR_NAME].astype(str)


# ------------------------- DISPLAY HELPERS -------------------------

LABELS = {
    k: v
    for k, v in {
        TITLE: "Title",
        YEAR: "Release Year",
        REVENUE: "Revenue",
        BUDGET: "Budget",
        RATING: "Rating",
        VOTES: "Votes",
        POPULARITY: "Popularity",
        ACTOR_NAME: "Actor",
        "genre_name": "Genre",
        GENRE_NAME: "Genre",
        "total_movies": "Total Movies",
        "average_rating": "Average Rating",
        "average_budget": "Average Budget",
        "average_revenue": "Average Revenue",
    }.items()
    if k
}


def label(col):
    return LABELS.get(col, col)


def prettify(df):
    """Friendly column names, integer years, no internal ID columns."""
    out = df.copy()
    drop_cols = [c for c in [PERSON_ID, MOVIE_ID] if c and c in out.columns]
    out = out.drop(columns=drop_cols)
    if YEAR in out.columns:
        out[YEAR] = out[YEAR].round().astype("Int64")
    return out.rename(columns=LABELS)


def column_config_for(df):
    cfg = {}
    for c in df.columns:
        if c in ("Revenue", "Budget", "Average Budget", "Average Revenue"):
            cfg[c] = st.column_config.NumberColumn(c, format="$%,.0f")
        elif c in ("Rating", "Average Rating"):
            cfg[c] = st.column_config.NumberColumn(c, format="%.1f")
        elif c == "Release Year":
            cfg[c] = st.column_config.NumberColumn(c, format="%d")
        elif c == "Popularity":
            cfg[c] = st.column_config.NumberColumn(c, format="%.1f")
    return cfg


def show_table(df, key, csv_name, csv_label, max_height=420):
    """Download button (left) and search box (right) on one row, then a scrollable table."""
    dl_col, s_col = st.columns([2, 1])

    with s_col:
        query = st.text_input(
            "Search table", key=f"search_{key}",
            placeholder="🔍 Search table...",
            label_visibility="collapsed",
        )

    shown = df
    if query:
        mask = (
            df.astype(str)
            .apply(lambda c: c.str.contains(query, case=False, na=False, regex=False))
            .any(axis=1)
        )
        shown = df[mask]

    with dl_col:
        csv_download_button(shown, csv_name, csv_label, key=f"dl_{key}")

    st.caption(f"Showing {len(shown):,} of {len(df):,} rows")
    if shown.empty:
        st.info("No rows match your search.")
        return

    needed = 35 * (len(shown) + 1) + 3
    st.dataframe(
        shown,
        use_container_width=True,
        hide_index=True,
        height=min(needed, max_height),
        column_config=column_config_for(shown),
    )


def format_currency(value):
    if pd.isna(value):
        return "N/A"
    if abs(value) >= 1_000_000_000:
        return f"${value / 1_000_000_000:,.2f}B"
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:,.2f}M"
    return f"${value:,.0f}"


def csv_download_button(df, filename, button_label, key=None):
    st.download_button(
        label=button_label,
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name=filename,
        mime="text/csv",
        key=key,
    )


def style_fig(fig, title, height, margin=None):
    fig.update_layout(
        template="plotly_white",
        title={"text": title, "font": {"size": 16, "color": "#18243A"}},
        font={"family": "Inter", "size": 12, "color": "#42536A"},
        height=height,
        margin=margin or dict(l=15, r=25, t=55, b=35),
    )
    return fig


PLOT_CONFIG = {
    "displayModeBar": "hover",
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
    "toImageButtonOptions": {"format": "png", "scale": 2},
}


def show_fig(fig):
    st.plotly_chart(fig, use_container_width=True, config=PLOT_CONFIG)


def display_bar(df, x, y, title, horizontal=False, height=320, fixed_height=False):
    if df.empty:
        st.info("No data available for this chart.")
        return

    value_col = x if horizontal else y
    vmax = max(float(df[value_col].max()), 1.0)

    # Short, readable bar labels (e.g. $2.92B) so nothing gets cut off
    if vmax >= 1_000_000:
        texts = [format_currency(v) for v in df[value_col]]
    elif vmax < 100:
        texts = [f"{v:,.2f}" for v in df[value_col]]
    else:
        texts = [f"{v:,.0f}" for v in df[value_col]]
    vfmt = ",.0f" if vmax >= 100 else ",.2f"

    if horizontal:
        fig = px.bar(df, x=x, y=y, orientation="h")
        fig.update_layout(yaxis={"categoryorder": "total ascending"}, yaxis_title=None)
        fig.update_xaxes(range=[0, vmax * 1.3])  # headroom for the labels
        fig.update_traces(
            hovertemplate=f"<b>%{{y}}</b><br>{x}: %{{x:{vfmt}}}<extra></extra>"
        )
        if not fixed_height:
            height = max(height, 36 * len(df) + 110)
    else:
        fig = px.bar(df, x=x, y=y)
        fig.update_layout(xaxis_title=None)
        fig.update_yaxes(range=[0, vmax * 1.2])
        fig.update_traces(
            hovertemplate=f"<b>%{{x}}</b><br>{y}: %{{y:{vfmt}}}<extra></extra>"
        )

    fig.update_traces(
        text=texts, textposition="outside", cliponaxis=False,
        marker_color="#3F6AA8",
    )
    fig.update_layout(showlegend=False)
    style_fig(fig, title, height)
    show_fig(fig)


def display_line(df, x, y, title, height=320):
    if df.empty:
        st.info("No data available for this chart.")
        return
    fig = px.line(df, x=x, y=y, markers=True)
    fig.update_traces(line=dict(width=2), marker=dict(size=6))
    fig.update_layout(hovermode="x unified")
    style_fig(fig, title, height)
    show_fig(fig)


def display_donut(df, category, value, title, height=460):
    if df.empty:
        st.info("No data available for this chart.")
        return

    data = df[[category, value]].dropna().sort_values(value, ascending=False).copy()
    total = data[value].sum()
    if total <= 0:
        st.info("No data available for this chart.")
        return

    # Percentage sits next to every legend label, so nothing overlaps on the ring
    data["_label"] = (
        data[category].astype(str)
        + "  ("
        + (data[value] / total * 100).round(1).astype(str)
        + "%)"
    )

    fig = px.pie(data, names="_label", values=value, hole=0.5)
    fig.update_traces(
        sort=False,
        textinfo="percent",
        textposition="inside",
        insidetextorientation="horizontal",
        marker=dict(line=dict(color="#FFFFFF", width=1.5)),
        hovertemplate="<b>%{label}</b><br>Value: %{value:,.0f}<extra></extra>",
    )
    style_fig(fig, title, height, dict(l=10, r=10, t=55, b=15))
    fig.update_layout(
        uniformtext=dict(minsize=10, mode="hide"),  # hide % text on slices too small to fit
        legend=dict(
            orientation="v", x=1.0, y=0.5, xanchor="left", yanchor="middle",
            font=dict(size=11), tracegroupgap=2,
        ),
    )
    show_fig(fig)


def display_scatter(df, x, y, title, hover=None, height=320):
    if df.empty:
        st.info("No data available for this chart.")
        return
    fig = px.scatter(df, x=x, y=y, hover_name=hover, opacity=0.7)
    style_fig(fig, title, height)
    show_fig(fig)


# ------------------------- FILTER LOGIC -------------------------

def apply_filters(source, genres_sel, years, min_rating, language, min_votes):
    out = source.copy()

    if HAS_YEAR and years:
        out = out[out[YEAR].between(years[0], years[1], inclusive="both").fillna(False)]

    out = out[out[RATING].fillna(0) >= min_rating]

    if VOTES and min_votes > 0:
        out = out[out[VOTES].fillna(0) >= min_votes]

    if language != "All Languages" and LANGUAGE:
        out = out[out[LANGUAGE].astype(str) == language]

    if genres_sel:
        ids = movie_genre_data[movie_genre_data[GENRE_NAME].isin(genres_sel)][
            MG_MOVIE_ID
        ].unique()
        out = out[out[MOVIE_ID].isin(ids)]

    return out


def get_filtered_relationships(filtered):
    ids = filtered[MOVIE_ID].dropna().unique()
    return movie_genre_data[movie_genre_data[MG_MOVIE_ID].isin(ids)].copy()


def genre_summary(filtered):
    rel = get_filtered_relationships(filtered)
    if rel.empty:
        return pd.DataFrame(columns=[GENRE_NAME, "total_movies", "average_rating"])

    summary = (
        rel.groupby(GENRE_NAME)
        .agg(total_movies=(MG_MOVIE_ID, "nunique"))
        .reset_index()
    )
    rated = rel.merge(
        filtered[[MOVIE_ID, RATING]],
        left_on=MG_MOVIE_ID, right_on=MOVIE_ID, how="left",
    )
    avg = rated.groupby(GENRE_NAME)[RATING].mean().reset_index(name="average_rating")
    return summary.merge(avg, on=GENRE_NAME, how="left").sort_values(
        "total_movies", ascending=False
    )


# ------------------------- SESSION STATE -------------------------

def year_bounds():
    return int(movies[YEAR].min()), int(movies[YEAR].max())


def reset_filters():
    st.session_state["selected_genres"] = []
    st.session_state["selected_language"] = "All Languages"
    st.session_state["minimum_rating"] = 0.0
    st.session_state["minimum_votes"] = 0
    if HAS_YEAR:
        st.session_state["selected_years"] = year_bounds()


st.session_state.setdefault("selected_genres", [])
st.session_state.setdefault("selected_language", "All Languages")
st.session_state.setdefault("minimum_rating", 0.0)
st.session_state.setdefault("minimum_votes", 0)
st.session_state.setdefault(
    "selected_years", year_bounds() if HAS_YEAR else (1900, 2030)
)


# ------------------------- SIDEBAR -------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding:0 0 4px;">
            <div style="font-size:22px;font-weight:700;color:white;">🎬 Reel Insights</div>
            <div style="font-size:11px;color:#AAB8CC;">MOVIE INDUSTRY ANALYTICS</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sb-label">NAVIGATION</div>', unsafe_allow_html=True)
    page = st.radio(
        "Choose page", ["Dashboard", "Query Explorer"],
        key="page", label_visibility="collapsed",
    )

    st.markdown('<div class="sb-label sb-gap">FILTERS</div>', unsafe_allow_html=True)

    genre_options = sorted(genres[GENRE_NAME].dropna().astype(str).unique().tolist())
    selected_genres = st.multiselect(
        "Movie Genre", options=genre_options,
        key="selected_genres", placeholder="All genres",
    )

    if HAS_YEAR:
        lo, hi = year_bounds()
        selected_years = st.slider("Release Year", min_value=lo, max_value=hi, key="selected_years")
    else:
        selected_years = (1900, 2030)

    minimum_rating = st.slider(
        "Minimum Rating", min_value=0.0, max_value=10.0, step=0.5, key="minimum_rating"
    )

    if VOTES:
        vote_cap = int(min(5000, max(100, movies[VOTES].max(skipna=True) or 100)))
        minimum_votes = st.slider(
            "Minimum Votes", min_value=0, max_value=vote_cap, step=10,
            key="minimum_votes",
            help="Hides movies with very few votes, whose ratings are unreliable.",
        )
    else:
        minimum_votes = 0

    language_options = (
        sorted(movies[LANGUAGE].dropna().astype(str).unique().tolist()) if LANGUAGE else []
    )
    selected_language = st.selectbox(
        "Original Language", options=["All Languages"] + language_options,
        key="selected_language",
    )

    st.button("↻ Reset All Filters", on_click=reset_filters, use_container_width=True)
    st.caption("Filters apply to both pages.")


loader = st.empty()
loader.markdown(
    '<div class="rl-loader"><div class="rl-spinner"></div>'
    '<div class="rl-text">Loading data…</div></div>',
    unsafe_allow_html=True,
)

filtered_movies = apply_filters(
    movies, selected_genres, selected_years,
    minimum_rating, selected_language, minimum_votes,
)

if CAST_MOVIE_ID:
    filtered_cast = cast[cast[CAST_MOVIE_ID].isin(filtered_movies[MOVIE_ID])].copy()
else:
    filtered_cast = cast.copy()


# ------------------------- COMMON UI -------------------------

def page_header(title, subtitle, icon="📊"):
    st.markdown(
        f"""
        <div class="page-header">
            <div class="ph-icon">{icon}</div>
            <div><h1>{title}</h1><p>{subtitle}</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def active_filters_text():
    parts = [
        "Genres: " + (", ".join(selected_genres) if selected_genres else "All"),
    ]
    if HAS_YEAR:
        parts.append(f"{selected_years[0]}–{selected_years[1]}")
    parts.append(f"Rating ≥ {minimum_rating:g}")
    if VOTES and minimum_votes > 0:
        parts.append(f"Votes ≥ {minimum_votes:,}")
    if selected_language != "All Languages":
        parts.append(f"Language: {selected_language}")
    return "Active filters: " + " · ".join(parts)


def revenue_chart_data(filtered):
    if not REVENUE:
        return pd.DataFrame()
    data = filtered[filtered[REVENUE] > 0]
    return (
        data.nlargest(10, REVENUE)[[TITLE, REVENUE]].sort_values(REVENUE, ascending=True)
    )


# Empty state: stop early with a clear message
if filtered_movies.empty:
    page_header(
        "Dashboard Overview" if page == "Dashboard" else "Query Explorer",
        "No data to display.",
        icon="⚠️",
    )
    loader.empty()
    st.warning("No movies match the selected filters. Try widening them or reset all filters.")
    st.stop()


# ------------------------- DASHBOARD PAGE -------------------------

if page == "Dashboard":
    page_header(
        "Dashboard Overview",
        "Explore movie performance, genres, ratings and financial insights.",
        icon="📊",
    )
    st.caption(active_filters_text())

    genre_data = genre_summary(filtered_movies)

    total_movies = filtered_movies[MOVIE_ID].nunique()
    total_genres = genre_data[GENRE_NAME].nunique() if not genre_data.empty else 0
    total_actors = filtered_cast[PERSON_ID].nunique() if HAS_CAST and not filtered_cast.empty else None
    average_rating = filtered_movies[RATING].mean()

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Movies", f"{total_movies:,}")
    k2.metric("Genres Represented", f"{total_genres:,}")
    k3.metric("Total Actors", f"{total_actors:,}" if total_actors is not None else "N/A")
    k4.metric("Average Rating", f"{average_rating:.2f}/10" if pd.notna(average_rating) else "N/A")

    dl_col, count_col = st.columns([1, 3])
    with dl_col:
        csv_download_button(
            prettify(filtered_movies),
            "reel_insights_filtered_movies.csv",
            "⬇ Download Movie Details",
            key="dl_movies",
        )
    with count_col:
        st.caption(f"Showing {len(filtered_movies):,} filtered movie records.")

    st.divider()

    chart_h = max(460, 24 * len(genre_data) + 90) if not genre_data.empty else 460
    left, right = st.columns(2)

    with left:
        revenue_data = revenue_chart_data(filtered_movies)
        if not revenue_data.empty:
            view = prettify(revenue_data)
            display_bar(
                view, label(REVENUE), label(TITLE),
                "Top 10 Movies by Revenue ($)", horizontal=True,
                height=chart_h, fixed_height=True,
            )
        else:
            st.info("Revenue data is not available.")

    with right:
        if not genre_data.empty:
            display_donut(
                genre_data.rename(columns=LABELS),
                "Genre", "Total Movies", "Movies by Genre", height=chart_h,
            )
            if selected_genres:
                st.caption(
                    "Movies can belong to several genres, so related genres "
                    "also appear when you filter by one."
                )
        else:
            st.info("Genre data is not available.")

    st.divider()

    if BUDGET and REVENUE:
        fin = filtered_movies.dropna(subset=[BUDGET, REVENUE])
        fin = fin[(fin[BUDGET] > 0) & (fin[REVENUE] > 0)]
        if not fin.empty:
            sc = fin[[TITLE, BUDGET, REVENUE]].copy()
            sc["Budget ($ Millions)"] = sc[BUDGET] / 1_000_000
            sc["Revenue ($ Millions)"] = sc[REVENUE] / 1_000_000
            display_scatter(
                sc, "Budget ($ Millions)", "Revenue ($ Millions)",
                "Budget vs Revenue", hover=TITLE, height=380,
            )
        else:
            st.info("No positive budget and revenue records for the selected filters.")
    else:
        st.info("Budget or revenue columns are not available.")

    st.divider()

    st.markdown("#### Genre Performance Summary")
    if not genre_data.empty:
        genre_table = genre_data.rename(columns=LABELS).round(2)
        show_table(genre_table, "genre", "reel_insights_genre_summary.csv",
                   "⬇ Download Genre Summary")

    st.markdown("#### 💡 Key Insights")
    c1, c2 = st.columns(2)

    with c1:
        if REVENUE:
            rev = filtered_movies.dropna(subset=[REVENUE])
            if not rev.empty:
                m = rev.loc[rev[REVENUE].idxmax()]
                st.info(f"**Highest Revenue:** {m[TITLE]} ({format_currency(m[REVENUE])})")
        rated = filtered_movies.dropna(subset=[RATING])
        if not rated.empty:
            m = rated.loc[rated[RATING].idxmax()]
            st.info(f"**Highest Rated:** {m[TITLE]} ({m[RATING]:.2f}/10)")

    with c2:
        if not genre_data.empty:
            top = genre_data.iloc[0]
            st.info(
                f"**Most Popular Genre by Movie Count:** {top[GENRE_NAME]} "
                f"({int(top['total_movies']):,} movies)"
            )
        if pd.notna(average_rating):
            st.info(f"**Average Rating:** {average_rating:.2f}/10 across the filtered movies.")


# ------------------------- QUERY EXPLORER PAGE -------------------------

elif page == "Query Explorer":
    page_header(
        "Query Explorer",
        "Explore saved business questions, view results and download analysis data.",
        icon="🔎",
    )
    st.caption(active_filters_text())

    query_options = [
        "Top 10 Highest Revenue Movies",
        "Top 10 Highest Rated Movies",
        "Top 10 Most Popular Movies",
        "Movies Released by Year",
        "Genre Distribution",
        "Top 10 Actors by Movie Count",
        "Average Rating by Genre",
        "Movie Financial Summary",
    ]

    q_col, c_col = st.columns([2, 1])
    with q_col:
        selected_query = st.selectbox("Select Analysis", query_options, key="selected_query")
    with c_col:
        chart_choice = st.selectbox(
            "Chart Type",
            ["Auto (Recommended)", "Bar Chart", "Line Chart",
             "Donut Chart", "Scatter Plot", "No Chart"],
            key="chart_choice",
        )

    st.divider()

    result = pd.DataFrame()
    insight = "No insight available for this selection."
    note = None
    chart_x = chart_y = None
    horizontal_chart = False
    auto_chart = "bar"

    if selected_query == "Top 10 Highest Revenue Movies":
        if REVENUE:
            result = (
                filtered_movies[filtered_movies[REVENUE] > 0]
                .nlargest(10, REVENUE)[[TITLE, YEAR, REVENUE, RATING]]
            )
            chart_x, chart_y, horizontal_chart = REVENUE, TITLE, True
            if not result.empty:
                insight = (
                    f"**{result.iloc[0][TITLE]}** has the highest revenue "
                    f"({format_currency(result.iloc[0][REVENUE])}) in this selection."
                )

    elif selected_query == "Top 10 Highest Rated Movies":
        # Enforce a vote floor so 1-vote movies don't top the list
        vote_floor = max(minimum_votes, 100)
        pool = filtered_movies.dropna(subset=[RATING])
        if VOTES:
            pool = pool[pool[VOTES].fillna(0) >= vote_floor]
            note = f"Only movies with at least {vote_floor:,} votes are ranked."
        cols = [TITLE, YEAR, RATING] + ([VOTES] if VOTES else [])
        result = pool.nlargest(10, RATING)[cols]
        chart_x, chart_y, horizontal_chart = RATING, TITLE, True
        if not result.empty:
            insight = (
                f"**{result.iloc[0][TITLE]}** has the highest rating "
                f"({result.iloc[0][RATING]:.2f}/10) in this selection."
            )

    elif selected_query == "Top 10 Most Popular Movies":
        if POPULARITY:
            result = (
                filtered_movies.dropna(subset=[POPULARITY])
                .nlargest(10, POPULARITY)[[TITLE, YEAR, POPULARITY, RATING]]
            )
            chart_x, chart_y, horizontal_chart = POPULARITY, TITLE, True
            if not result.empty:
                insight = (
                    f"**{result.iloc[0][TITLE]}** has the highest popularity "
                    f"score ({result.iloc[0][POPULARITY]:.2f})."
                )

    elif selected_query == "Movies Released by Year":
        result = (
            filtered_movies.dropna(subset=[YEAR])
            .groupby(YEAR).agg(total_movies=(MOVIE_ID, "nunique"))
            .reset_index().sort_values(YEAR)
        )
        chart_x, chart_y, auto_chart = YEAR, "total_movies", "line"
        if not result.empty:
            peak = result.loc[result["total_movies"].idxmax()]
            insight = (
                f"The busiest release year is {int(peak[YEAR])}, "
                f"with {int(peak['total_movies']):,} movies."
            )

    elif selected_query == "Genre Distribution":
        result = genre_summary(filtered_movies).rename(columns={GENRE_NAME: "genre_name"})[
            ["genre_name", "total_movies", "average_rating"]
        ]
        chart_x, chart_y, horizontal_chart = "total_movies", "genre_name", True
        if not result.empty:
            best = result.iloc[0]
            insight = (
                f"**{best['genre_name']}** has the highest number of movies "
                f"({int(best['total_movies']):,}) in this selection."
            )

    elif selected_query == "Top 10 Actors by Movie Count":
        if HAS_CAST:
            actors = filtered_cast[[PERSON_ID, ACTOR_NAME, CAST_MOVIE_ID]].drop_duplicates(
                subset=[PERSON_ID, CAST_MOVIE_ID]
            )
            result = (
                actors.groupby([PERSON_ID, ACTOR_NAME])
                .agg(total_movies=(CAST_MOVIE_ID, "nunique"))
                .reset_index().sort_values("total_movies", ascending=False).head(10)
            )
            chart_x, chart_y, horizontal_chart = "total_movies", ACTOR_NAME, True
            if not result.empty:
                insight = (
                    f"**{result.iloc[0][ACTOR_NAME]}** has the most movie "
                    f"appearances ({int(result.iloc[0]['total_movies'])})."
                )
        else:
            st.warning(
                "Actor analysis needs person_id, actor_name and movie_id "
                "columns in the cast table."
            )

    elif selected_query == "Average Rating by Genre":
        result = (
            genre_summary(filtered_movies).rename(columns={GENRE_NAME: "genre_name"})[
                ["genre_name", "total_movies", "average_rating"]
            ]
            .dropna(subset=["average_rating"])
            .sort_values("average_rating", ascending=False)
        )
        chart_x, chart_y, horizontal_chart = "average_rating", "genre_name", True
        if not result.empty:
            best = result.iloc[0]
            insight = (
                f"**{best['genre_name']}** has the highest average rating "
                f"({best['average_rating']:.2f}/10) in this selection."
            )

    elif selected_query == "Movie Financial Summary":
        if BUDGET and REVENUE:
            fin = filtered_movies.dropna(subset=[YEAR, BUDGET, REVENUE])
            result = (
                fin.groupby(YEAR)
                .agg(
                    total_movies=(MOVIE_ID, "nunique"),
                    average_budget=(BUDGET, "mean"),
                    average_revenue=(REVENUE, "mean"),
                )
                .reset_index().sort_values(YEAR)
            )
            chart_x, chart_y, auto_chart = YEAR, "average_revenue", "line"
            if not result.empty:
                insight = (
                    "The table compares average production budget and "
                    "average revenue by release year."
                )

    if result.empty:
        st.warning("No results are available for this analysis and filter selection.")
    else:
        view = prettify(result).round(2)
        x_lbl = label(chart_x) if chart_x else None
        y_lbl = label(chart_y) if chart_y else None

        m_col, i_col = st.columns([1, 3])
        m_col.metric("Records returned", f"{len(view):,}")
        with i_col:
            st.caption(f"Analysis: {selected_query} · Current filters are applied")
            if note:
                st.caption(note)

        st.markdown("#### Query Results")
        show_table(view, "query", "reel_insights_query_results.csv",
                   "⬇ Download query results")

        chart_type = {
            "Bar Chart": "bar", "Line Chart": "line", "Donut Chart": "donut",
            "Scatter Plot": "scatter", "No Chart": "none",
            "Auto (Recommended)": auto_chart,
        }[chart_choice]

        st.markdown("#### Visualization")

        if chart_type == "none":
            st.caption("Chart is hidden. Choose another chart type to display a visualization.")

        elif chart_type == "bar":
            if x_lbl and y_lbl:
                display_bar(view, x_lbl, y_lbl, selected_query,
                            horizontal=horizontal_chart, height=320)
            else:
                st.info("A bar chart is not suitable for this result.")

        elif chart_type == "line":
            if x_lbl and y_lbl:
                display_line(view, x_lbl, y_lbl, selected_query, height=320)
            else:
                st.info("A line chart is not suitable for this result.")

        elif chart_type == "donut":
            category_col = next(
                (c for c in view.columns
                 if pd.api.types.is_string_dtype(view[c])
                 and not pd.api.types.is_numeric_dtype(view[c])),
                None,
            )
            numeric_col = next(
                (c for c in view.columns
                 if pd.api.types.is_numeric_dtype(view[c]) and c != "Release Year"),
                None,
            )
            if category_col and numeric_col:
                display_donut(view, category_col, numeric_col, selected_query, height=460)
            else:
                st.info("Donut chart requires one category column and one numeric column.")

        elif chart_type == "scatter":
            nums = [c for c in view.select_dtypes(include="number").columns]
            if len(nums) >= 2:
                hover = label(TITLE) if label(TITLE) in view.columns else None
                display_scatter(view, nums[0], nums[1], f"{nums[0]} vs {nums[1]}",
                                hover=hover, height=320)
            else:
                st.info("Scatter plot requires at least two numeric columns.")

        st.markdown("#### 💡 Analysis Insight")
        st.info(insight)



loader.empty()

# ------------------------- BOTTOM NAVIGATION -------------------------

def go_to(target):
    st.session_state["page"] = target


st.divider()
nav_left, nav_mid, nav_right = st.columns(3)

with nav_left:
    if page == "Query Explorer":
        st.button("← Dashboard", on_click=go_to, args=("Dashboard",),
                  use_container_width=True, key="nav_prev")

with nav_mid:
    components.html(
        """
        <button onclick="
            const d = window.parent.document;
            const m = d.querySelector('[data-testid=stMain]') || d.querySelector('section.main');
            if (m) m.scrollTo({top: 0, behavior: 'smooth'});
        " style="width:100%;height:40px;border:1px solid #D5DCE8;border-radius:8px;
                 background:#FFFFFF;color:#253247;font:500 14px Inter,sans-serif;cursor:pointer;">
            ↑ Back to top
        </button>
        """,
        height=46,
    )

with nav_right:
    if page == "Dashboard":
        st.button("Query Explorer →", on_click=go_to, args=("Query Explorer",),
                  use_container_width=True, key="nav_next")

# ------------------------- FOOTER -------------------------

st.markdown("---")
st.caption("Reel Insights · Movie Industry Analytics")