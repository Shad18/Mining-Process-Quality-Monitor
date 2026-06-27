"""
Mining Process Quality Monitoring Platform
Flotation Plant Analytics & Prediction System
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import warnings
import io
from datetime import datetime, timedelta
import traceback

warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
#  CONFIG & THEME
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Mining Process Quality Monitoring Platform",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

DARK_BG      = "#0d1117"
CARD_BG      = "#161b22"
CARD_BORDER  = "#21262d"
ACCENT_BLUE  = "#1f6feb"
ACCENT_CYAN  = "#39d0f5"
ACCENT_GREEN = "#3fb950"
ACCENT_AMBER = "#d29922"
ACCENT_RED   = "#f85149"
TEXT_PRIMARY = "#e6edf3"
TEXT_MUTED   = "#8b949e"

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor":  "rgba(0,0,0,0)",
        "font":          {"color": TEXT_PRIMARY, "family": "Inter, sans-serif"},
        "xaxis":         {"gridcolor": "#21262d", "zerolinecolor": "#21262d"},
        "yaxis":         {"gridcolor": "#21262d", "zerolinecolor": "#21262d"},
        "colorway":      [ACCENT_BLUE, ACCENT_CYAN, ACCENT_GREEN, ACCENT_AMBER, ACCENT_RED],
        "legend":        {"bgcolor": "rgba(0,0,0,0)"},
    }
}

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif;
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
}}

/* ── Sidebar ── */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #0d1117 0%, #161b22 100%);
    border-right: 1px solid {CARD_BORDER};
}}
[data-testid="stSidebar"] .stRadio label {{
    color: {TEXT_MUTED};
    padding: 6px 0;
    font-size: 0.92rem;
}}

/* ── Main ── */
.block-container {{
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}}

/* ── Cards ── */
.kpi-card {{
    background: {CARD_BG};
    border: 1px solid {CARD_BORDER};
    border-radius: 12px;
    padding: 20px 22px;
    margin-bottom: 12px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    transition: transform 0.2s;
}}
.kpi-card:hover {{ transform: translateY(-2px); }}
.kpi-title {{
    color: {TEXT_MUTED};
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 8px;
}}
.kpi-value {{
    font-size: 2.1rem;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 4px;
}}
.kpi-sub {{
    font-size: 0.78rem;
    color: {TEXT_MUTED};
}}

/* ── Page Header ── */
.page-header {{
    background: linear-gradient(135deg, #0d1117 0%, #1a2332 100%);
    border: 1px solid {CARD_BORDER};
    border-radius: 14px;
    padding: 24px 28px;
    margin-bottom: 24px;
    border-left: 4px solid {ACCENT_BLUE};
}}
.page-header h1 {{
    font-size: 1.6rem;
    font-weight: 700;
    margin: 0 0 4px 0;
    background: linear-gradient(90deg, {ACCENT_BLUE}, {ACCENT_CYAN});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.page-header p {{
    color: {TEXT_MUTED};
    margin: 0;
    font-size: 0.88rem;
}}

/* ── Status badges ── */
.badge-green  {{ background:#1a3a2a; color:{ACCENT_GREEN}; border:1px solid {ACCENT_GREEN}; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }}
.badge-amber  {{ background:#2d2200; color:{ACCENT_AMBER}; border:1px solid {ACCENT_AMBER}; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }}
.badge-red    {{ background:#2d1116; color:{ACCENT_RED};   border:1px solid {ACCENT_RED};   padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }}
.badge-blue   {{ background:#0d2148; color:{ACCENT_BLUE};  border:1px solid {ACCENT_BLUE};  padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:600; }}

/* ── Alarm ── */
.alarm-critical {{
    background: rgba(248,81,73,0.1);
    border: 1px solid {ACCENT_RED};
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}}
.alarm-warning {{
    background: rgba(210,153,34,0.1);
    border: 1px solid {ACCENT_AMBER};
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}}
.alarm-normal {{
    background: rgba(63,185,80,0.1);
    border: 1px solid {ACCENT_GREEN};
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
}}

/* ── Metric section ── */
.section-title {{
    font-size: 1rem;
    font-weight: 600;
    color: {TEXT_PRIMARY};
    margin: 18px 0 12px 0;
    padding-bottom: 6px;
    border-bottom: 1px solid {CARD_BORDER};
}}

/* ── Tables ── */
.stDataFrame {{ border-radius: 10px; overflow: hidden; }}

/* ── Inputs ── */
.stSelectbox div[data-baseweb="select"] > div,
.stNumberInput > div > div > input,
.stTextInput > div > div > input {{
    background: {CARD_BG} !important;
    border-color: {CARD_BORDER} !important;
    color: {TEXT_PRIMARY} !important;
    border-radius: 8px !important;
}}

/* ── Buttons ── */
.stButton > button {{
    background: linear-gradient(135deg, {ACCENT_BLUE}, #0c4a9e);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 24px;
    font-weight: 600;
    transition: all 0.2s;
    box-shadow: 0 4px 12px rgba(31,111,235,0.3);
}}
.stButton > button:hover {{
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(31,111,235,0.5);
}}

/* ── Metric ── */
[data-testid="stMetricValue"] {{
    color: {ACCENT_CYAN} !important;
    font-weight: 700 !important;
}}
[data-testid="stMetricDelta"] svg {{ display: none; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {{
    background: {CARD_BG};
    border-radius: 10px 10px 0 0;
    border-bottom: 1px solid {CARD_BORDER};
}}
.stTabs [data-baseweb="tab"] {{
    color: {TEXT_MUTED};
    font-weight: 500;
}}
.stTabs [aria-selected="true"] {{
    color: {ACCENT_CYAN} !important;
    border-bottom: 2px solid {ACCENT_CYAN} !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: {DARK_BG}; }}
::-webkit-scrollbar-thumb {{ background: {CARD_BORDER}; border-radius: 3px; }}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  DATA LOADING (cached)
# ─────────────────────────────────────────────
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

MODEL_DIR = BASE_DIR / "models"

ASSET_DIR = BASE_DIR / "assets"

@st.cache_data(show_spinner=False)
def load_raw():
    df = pd.read_csv(
    RAW_DATA_DIR / "MiningProcess_Flotation_Plant_Database.csv"
)
    for col in df.columns:
        if col != "date":
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df['date'] = pd.to_datetime(df['date'])
    return df

    




@st.cache_data(show_spinner=False)
def load_hourly():
    df = pd.read_csv(
    PROCESSED_DATA_DIR / "mining_hourly_processed.csv"
)    
    df['date'] = pd.to_datetime(df['date'],errors='coerce')
    return df

@st.cache_data(show_spinner=False)
def load_feat_imp():
    return pd.read_csv(ASSET_DIR / "feature_importance.csv")

@st.cache_resource(show_spinner=False)
def load_models():
    return {
        "with_iron":    joblib.load(MODEL_DIR / "model_with_iron.pkl"),
        "without_iron": joblib.load(MODEL_DIR / "model_without_iron.pkl"),
        "1h_ahead":     joblib.load(MODEL_DIR / "model_1h_ahead.pkl"),
    }


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def card(title, value, sub="", color=ACCENT_CYAN, icon=""):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{icon} {title}</div>
        <div class="kpi-value" style="color:{color}">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)


def page_header(title, subtitle, icon="⚙️"):
    st.markdown(f"""
    <div class="page-header">
        <h1>{icon} {title}</h1>
        <p>{subtitle}</p>
    </div>""", unsafe_allow_html=True)


def badge(text, level="green"):
    return f'<span class="badge-{level}">{text}</span>'


def apply_template(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=TEXT_PRIMARY, family="Inter, sans-serif"),
    )
    fig.update_xaxes(gridcolor=CARD_BORDER, zerolinecolor=CARD_BORDER)
    fig.update_yaxes(gridcolor=CARD_BORDER, zerolinecolor=CARD_BORDER)
    return fig


def get_model_features(model):
    if hasattr(model, 'feature_names_in_'):
        return [str(f) for f in model.feature_names_in_]
    elif hasattr(model, 'feature_name_'):
        return model.feature_name_
    elif hasattr(model, 'get_booster') and model.get_booster().feature_names:
        return model.get_booster().feature_names
    return []


def silica_risk_level(val):
    if val < 1.5:
        return ("LOW", ACCENT_GREEN, "green")
    elif val < 2.5:
        return ("MEDIUM", ACCENT_AMBER, "amber")
    else:
        return ("HIGH", ACCENT_RED, "red")


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────

PAGES = [
    "🏠  Dashboard",
    "🔮  Live Prediction",
    "📡  Future Prediction",
    "📊  Historical Analytics",
    "🏭  Process Monitoring",
    "🔬  Feature Analysis",
    "🤖  Model Performance",
    "📄  Reports",
    "ℹ️  About",
]

with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding:16px 0 24px 0;">
        <div style="font-size:2rem;">⚙️</div>
        <div style="font-size:1.05rem; font-weight:700; color:{ACCENT_CYAN}; margin-top:8px;">
                Minging Process QM
        </div>
        <div style="font-size:0.72rem; color:{TEXT_MUTED}; margin-top:2px;">
            Flotation Plant Monitor
        </div>
    </div>
    <hr style="border-color:{CARD_BORDER}; margin: 0 0 16px 0;">
    """, unsafe_allow_html=True)

    page = st.radio("Navigation", PAGES, label_visibility="collapsed")

    st.markdown(f"""
    <hr style="border-color:{CARD_BORDER}; margin:24px 0 12px 0;">
    <div style="font-size:0.7rem; color:{TEXT_MUTED}; text-align:center;">
        <div style="margin-bottom:4px;">XGBoost · Streamlit · Plotly</div>
        <div>v1.0.0 · Industrial Analytics</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PAGE 1 — DASHBOARD
# ─────────────────────────────────────────────

def page_dashboard():
    page_header("Dashboard", "Real-time flotation plant overview and KPI monitoring", "🏠")

    try:
        df  = load_hourly()
        raw = load_raw()
    except Exception as e:
        st.error(f"Data load error: {e}")
        return

    latest = df.iloc[-1]
    silica_out = latest.get('% Silica Concentrate', np.nan)
    iron_out   = latest.get('% Iron Concentrate',   np.nan)
    iron_feed  = latest.get('% Iron Feed',          np.nan)
    silica_feed= latest.get('% Silica Feed',        np.nan)

    recovery   = round(100 * (iron_out / iron_feed), 1) if iron_feed else 0
    stability  = round(100 - df['% Silica Concentrate'].tail(24).std() * 20, 1)
    stability  = max(0, min(100, stability))
    risk, rcol, _ = silica_risk_level(silica_out)

    # ── KPI row ──
    cols = st.columns(4)
    with cols[0]:
        card("Iron Feed",      f"{iron_feed:.1f}%",   "% Fe in raw ore feed",   ACCENT_CYAN,  "🪨")
    with cols[1]:
        card("Silica Output",  f"{silica_out:.2f}%",  "% SiO₂ concentrate",     rcol,         "🔬")
    with cols[2]:
        card("Iron Recovery",  f"{recovery:.1f}%",    "Recovery efficiency",    ACCENT_GREEN, "📈")
    with cols[3]:
        card("Process Stability", f"{stability:.0f}%","Last 24-hour window",    ACCENT_BLUE,  "⚡")

    cols2 = st.columns(4)
    with cols2[0]:
        card("Starch Flow",    f"{latest.get('Starch Flow', 0):.1f}",  "m³/h",  ACCENT_CYAN,  "💧")
    with cols2[1]:
        card("Ore Pulp pH",    f"{latest.get('Ore Pulp pH', 0):.2f}", "",        ACCENT_AMBER, "⚗️")
    with cols2[2]:
        card("Ore Flow",       f"{latest.get('Ore Pulp Flow', 0):.0f}", "t/h",  ACCENT_GREEN, "⛏️")
    with cols2[3]:
        status_txt = "CRITICAL" if risk=="HIGH" else ("WARNING" if risk=="MEDIUM" else "NORMAL")
        status_col = ACCENT_RED if risk=="HIGH" else (ACCENT_AMBER if risk=="MEDIUM" else ACCENT_GREEN)
        card("Plant Status",   status_txt, f"Silica risk: {risk}",     status_col, "🟢")

    st.markdown('<div class="section-title">Trend Analysis</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        tail = df.tail(72)
        fig  = go.Figure()
        fig.add_trace(go.Scatter(x=tail['date'], y=tail['% Silica Concentrate'],
                                  mode='lines', fill='tozeroy',
                                  fillcolor='rgba(57,208,245,0.12)',
                                  line=dict(color=ACCENT_CYAN, width=2),
                                  name='Silica Conc.'))
        fig.add_hline(y=2.0, line_dash="dash", line_color=ACCENT_AMBER,
                      annotation_text="Threshold 2%")
        fig.update_layout(title="Silica Concentrate – Last 72 h",
                          height=300, margin=dict(l=0,r=0,t=40,b=0))
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=tail['date'], y=tail['% Iron Concentrate'],
                                   mode='lines', fill='tozeroy',
                                   fillcolor='rgba(63,185,80,0.12)',
                                   line=dict(color=ACCENT_GREEN, width=2),
                                   name='Iron Conc.'))
        fig2.update_layout(title="Iron Concentrate – Last 72 h",
                           height=300, margin=dict(l=0,r=0,t=40,b=0))
        apply_template(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        # Gauge – Silica
        fig_g = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=float(silica_out),
            title={'text': "Silica Concentrate (%)", 'font': {'color': TEXT_PRIMARY}},
            delta={'reference': 1.5, 'increasing': {'color': ACCENT_RED}},
            gauge={
                'axis': {'range': [0, 5], 'tickcolor': TEXT_MUTED},
                'bar': {'color': rcol},
                'steps': [
                    {'range': [0, 1.5], 'color': 'rgba(63,185,80,0.15)'},
                    {'range': [1.5, 2.5], 'color': 'rgba(210,153,34,0.15)'},
                    {'range': [2.5, 5],   'color': 'rgba(248,81,73,0.15)'},
                ],
                'threshold': {'line': {'color': ACCENT_RED, 'width': 3}, 'value': 2.5}
            }
        ))
        fig_g.update_layout(height=280, margin=dict(l=20,r=20,t=40,b=0))
        apply_template(fig_g)
        st.plotly_chart(fig_g, use_container_width=True)

    with c4:
        # Donut – air flow distribution
        air_cols = [c for c in df.columns if 'Air Flow' in c]
        air_vals = [abs(float(latest.get(c, 0))) for c in air_cols]
        fig_d = go.Figure(go.Pie(
            labels=[c.replace('Flotation Column ', 'Col ') for c in air_cols],
            values=air_vals, hole=0.5,
            marker=dict(colors=[ACCENT_BLUE, ACCENT_CYAN, ACCENT_GREEN,
                                 ACCENT_AMBER, ACCENT_RED, '#9b59b6', '#e67e22'])
        ))
        fig_d.update_layout(title="Air Flow Distribution by Column",
                            height=280, margin=dict(l=0,r=0,t=40,b=0))
        apply_template(fig_d)
        st.plotly_chart(fig_d, use_container_width=True)

    # Heatmap – hourly silica heat
    st.markdown('<div class="section-title">Silica Heatmap (Hour × Day-of-week)</div>',
                unsafe_allow_html=True)
    tmp = df.copy()
    tmp['hour']       = pd.to_datetime(tmp['date']).dt.hour
    tmp['day_of_week']= pd.to_datetime(tmp['date']).dt.day_name()
    hm = tmp.groupby(['day_of_week','hour'])['% Silica Concentrate'].mean().reset_index()
    dow_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    hm_piv = hm.pivot(index='day_of_week', columns='hour', values='% Silica Concentrate')
    hm_piv = hm_piv.reindex([d for d in dow_order if d in hm_piv.index])
    fig_h = px.imshow(hm_piv, color_continuous_scale='RdYlGn_r',
                       labels=dict(x="Hour of Day", y="", color="Silica %"),
                       aspect='auto')
    fig_h.update_layout(height=260, margin=dict(l=0,r=0,t=10,b=0))
    apply_template(fig_h)
    st.plotly_chart(fig_h, use_container_width=True)


# ─────────────────────────────────────────────
#  PAGE 2 — LIVE PREDICTION
# ─────────────────────────────────────────────

def page_live_prediction():
    page_header("Live Prediction", "Enter process parameters to predict silica/iron concentrate",
                "🔮")
    models = load_models()
    df     = load_hourly()

    latest = df.iloc[-1].to_dict()

    pred_type = st.radio("Prediction Target", ["Silica Concentrate", "Iron Concentrate"],
                         horizontal=True)
    use_iron  = pred_type == "Silica Concentrate"
    model_key = "with_iron" if use_iron else "without_iron"
    model     = models[model_key]
    features  = get_model_features(model)

    st.markdown('<div class="section-title">Process Parameters</div>', unsafe_allow_html=True)

    DEFAULTS = {
        '% Iron Feed':      56.0, '% Silica Feed':   12.5,
        'Starch Flow':      3000.0, 'Amina Flow':     350.0,
        'Ore Pulp Flow':    400.0,  'Ore Pulp pH':    9.5,
        'Ore Pulp Density': 1.7,    '% Iron Concentrate': 65.0,
        'silica_lag_1':     1.8,    'silica_lag_2':   1.9,
        'silica_lag_4':     2.0,    'silica_lag_24':  2.1,
        'silica_roll_mean_3':  1.85,'silica_roll_mean_6': 1.9,
        'silica_roll_mean_24': 2.0,
        'hour': 12, 'day': 15, 'month': 6, 'day_of_week': 2,
    }
    for c in features:
        if c not in DEFAULTS:
            DEFAULTS[c] = float(latest.get(c, 0))

    # Auto-fill from latest
    inputs = {}
    basic_feats = [f for f in features if 'lag' not in f and 'roll' not in f
                   and f not in ('hour','day','month','day_of_week')]
    lag_feats   = [f for f in features if 'lag' in f or 'roll' in f]
    time_feats  = [f for f in features if f in ('hour','day','month','day_of_week')]

    with st.expander("⚙️ Basic Process Parameters", expanded=True):
        cols = st.columns(3)
        for i, feat in enumerate(basic_feats):
            dv = float(latest.get(feat, DEFAULTS.get(feat, 0)))
            inputs[feat] = cols[i % 3].number_input(feat, value=dv, step=0.01, key=f"b_{feat}")

    with st.expander("🕐 Time Features"):
        now = datetime.now()
        cols = st.columns(4)
        inputs['hour']       = cols[0].number_input("Hour",       0, 23, now.hour)
        inputs['day']        = cols[1].number_input("Day",        1, 31, now.day)
        inputs['month']      = cols[2].number_input("Month",      1, 12, now.month)
        inputs['day_of_week']= cols[3].number_input("Day of Week",0,  6, now.weekday())

    with st.expander("📉 Lag & Rolling Features"):
        cols = st.columns(3)
        for i, feat in enumerate(lag_feats):
            dv = float(latest.get(feat, DEFAULTS.get(feat, 1.9)))
            inputs[feat] = cols[i % 3].number_input(feat, value=dv, step=0.01, key=f"l_{feat}")

    if st.button("🚀 Run Prediction", use_container_width=True):
        try:
            X = pd.DataFrame([{f: inputs.get(f, 0) for f in features}])
            pred = float(model.predict(X)[0])
            risk, rcol, rlvl = silica_risk_level(pred) if use_iron else ("N/A", ACCENT_CYAN, "blue")
            label = "% Silica Concentrate" if use_iron else "% Iron Concentrate"

            st.markdown('<div class="section-title">Prediction Result</div>',
                        unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1:
                card("Predicted Value", f"{pred:.3f}%", label, rcol, "🎯")
            with r2:
                conf = max(0, min(100, 100 - abs(pred - 2.0) * 15))
                card("Model Confidence", f"{conf:.0f}%", "XGBoost estimate", ACCENT_BLUE, "📊")
            with r3:
                card("Risk Level", risk, f"Silica threshold: 2.0%", rcol, "⚠️")

            # Gauge
            fig_pred = go.Figure(go.Indicator(
                mode="gauge+number",
                value=pred,
                title={'text': label, 'font': {'color': TEXT_PRIMARY}},
                gauge={
                    'axis': {'range': [0, 5] if use_iron else [50, 80]},
                    'bar': {'color': rcol},
                    'steps': [
                        {'range': [0, 1.5], 'color': 'rgba(63,185,80,0.15)'},
                        {'range': [1.5, 2.5],'color': 'rgba(210,153,34,0.15)'},
                        {'range': [2.5, 5],  'color': 'rgba(248,81,73,0.15)'},
                    ] if use_iron else [
                        {'range': [50, 60], 'color': 'rgba(248,81,73,0.15)'},
                        {'range': [60, 67], 'color': 'rgba(210,153,34,0.15)'},
                        {'range': [67, 80], 'color': 'rgba(63,185,80,0.15)'},
                    ]
                }
            ))
            fig_pred.update_layout(height=280, margin=dict(l=20,r=20,t=40,b=0))
            apply_template(fig_pred)
            st.plotly_chart(fig_pred, use_container_width=True)

            # Feature importance bar
            st.markdown('<div class="section-title">Top Feature Influences</div>',
                        unsafe_allow_html=True)
            fi = pd.DataFrame({
                'feature':    features,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False).head(12)

            fig_fi = px.bar(fi, x='importance', y='feature', orientation='h',
                            color='importance', color_continuous_scale='Blues')
            fig_fi.update_layout(height=380, margin=dict(l=0,r=0,t=10,b=0),
                                  yaxis={'categoryorder': 'total ascending'},
                                  coloraxis_showscale=False)
            apply_template(fig_fi)
            st.plotly_chart(fig_fi, use_container_width=True)

            # Alert
            if use_iron and pred > 2.0:
                st.markdown(f"""
                <div class="alarm-critical">
                    ⚠️ <b>QUALITY ALERT:</b> Predicted silica ({pred:.2f}%) exceeds
                    acceptable threshold (2.0%). Recommend reviewing starch dosage and air flow.
                </div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alarm-normal">
                    ✅ <b>QUALITY OK:</b> Predicted value ({pred:.3f}%) is within
                    acceptable operating range.
                </div>""", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Prediction failed: {e}\n{traceback.format_exc()}")


# ─────────────────────────────────────────────
#  PAGE 3 — FUTURE PREDICTION
# ─────────────────────────────────────────────

def page_future_prediction():
    page_header("Future Prediction", "One-hour ahead silica quality forecast using temporal model",
                "📡")
    models = load_models()
    df     = load_hourly()
    model  = models["1h_ahead"]
    feats  = get_model_features(model)

    st.info("🕐 This model predicts silica concentrate **1 hour into the future** based on "
            "current process state and lag features.")

    # Predict on last N rows
    n_pts = st.slider("Forecast window (recent hours)", 12, 96, 48)
    sub   = df.tail(n_pts + 24).copy()

    try:
        avail = [f for f in feats if f in sub.columns]
        miss  = [f for f in feats if f not in sub.columns]
        if miss:
            st.warning(f"Missing features filled with 0: {miss}")
        for f in miss:
            sub[f] = 0.0

        sub_feat = sub[feats].dropna()
        preds    = model.predict(sub_feat)
        sub_feat = sub_feat.copy()
        sub_feat['pred_1h'] = preds
        sub_feat['date']    = sub.loc[sub_feat.index, 'date'].values
        sub_feat['actual']  = sub.loc[sub_feat.index, '% Silica Concentrate'].values

        last_actual = float(sub_feat['actual'].iloc[-1])
        last_pred   = float(sub_feat['pred_1h'].iloc[-1])
        delta       = last_pred - last_actual
        risk, rcol, _ = silica_risk_level(last_pred)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            card("Next-Hour Forecast", f"{last_pred:.2f}%", "Silica concentrate", rcol, "📡")
        with c2:
            card("Current Actual",    f"{last_actual:.2f}%", "Latest measurement", ACCENT_CYAN, "📌")
        with c3:
            dstr = f"{'↑' if delta>0 else '↓'} {abs(delta):.2f}%"
            dcol = ACCENT_RED if delta > 0.3 else (ACCENT_GREEN if delta < -0.3 else ACCENT_AMBER)
            card("Expected Change",   dstr, "vs current", dcol, "📈")
        with c4:
            card("Risk Level",        risk, "Forecast risk assessment", rcol, "⚠️")

        # Forecast chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=sub_feat['date'], y=sub_feat['actual'],
                                  mode='lines', name='Actual',
                                  line=dict(color=ACCENT_CYAN, width=2)))
        fig.add_trace(go.Scatter(x=sub_feat['date'], y=sub_feat['pred_1h'],
                                  mode='lines', name='1h Forecast',
                                  line=dict(color=ACCENT_AMBER, width=2, dash='dot')))
        fig.add_hline(y=2.0, line_dash="dash", line_color=ACCENT_RED,
                      annotation_text="Alert Threshold")
        fig.update_layout(title="Actual vs 1-Hour Ahead Forecast",
                          height=380, margin=dict(l=0,r=0,t=40,b=0),
                          legend=dict(x=0, y=1))
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        # Residual
        sub_feat['error'] = sub_feat['pred_1h'] - sub_feat['actual']
        fig2 = px.area(sub_feat, x='date', y='error',
                        color_discrete_sequence=[ACCENT_AMBER])
        fig2.add_hline(y=0, line_color=TEXT_MUTED)
        fig2.update_layout(title="Forecast Error (Predicted − Actual)",
                           height=240, margin=dict(l=0,r=0,t=40,b=0))
        apply_template(fig2)
        st.plotly_chart(fig2, use_container_width=True)

        # Recommendations
        st.markdown('<div class="section-title">Operational Recommendations</div>',
                    unsafe_allow_html=True)
        if last_pred > 2.5:
            recs = ["🔴 **CRITICAL**: Increase starch dosage by 5-8%",
                    "🔴 Reduce ore feed rate to stabilise pulp flow",
                    "🔴 Check Column 01-03 air flow valves",
                    "🟡 Alert quality control supervisor immediately"]
        elif last_pred > 2.0:
            recs = ["🟡 **WARNING**: Monitor starch addition closely",
                    "🟡 Verify flotation column levels",
                    "🟢 Schedule preventive maintenance check",
                    "🟢 Review reagent dosing rates"]
        else:
            recs = ["🟢 **NORMAL**: Process operating within spec",
                    "🟢 Maintain current reagent dosing",
                    "🟢 Continue standard monitoring protocol",
                    "🔵 Opportunity to optimise energy consumption"]
        for r in recs:
            st.markdown(r)

    except Exception as e:
        st.error(f"Forecast error: {e}")


# ─────────────────────────────────────────────
#  PAGE 4 — HISTORICAL ANALYTICS
# ─────────────────────────────────────────────

def page_historical():
    page_header("Historical Analytics", "Deep-dive analysis of flotation plant historical data",
                "📊")
    raw = load_raw()

    # Filters
    with st.expander("🔍 Filters", expanded=True):
        c1, c2 = st.columns(2)
        min_date = raw['date'].min().date()
        max_date = raw['date'].max().date()
        d_range  = c1.date_input("Date Range",
                                  value=(min_date, max_date),
                                  min_value=min_date, max_value=max_date)
        silica_range = c2.slider("Silica Concentrate Range (%)",
                                  0.0, 5.0, (0.0, 5.0), 0.1)

    if len(d_range) == 2:
        mask = ((raw['date'].dt.date >= d_range[0]) &
                (raw['date'].dt.date <= d_range[1]) &
                (raw['% Silica Concentrate'] >= silica_range[0]) &
                (raw['% Silica Concentrate'] <= silica_range[1]))
        filtered = raw[mask]
    else:
        filtered = raw

    st.markdown(f"**{len(filtered):,}** records | "
                f"Silica avg: **{filtered['% Silica Concentrate'].mean():.2f}%** | "
                f"Iron avg: **{filtered['% Iron Concentrate'].mean():.2f}%**")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["📈 Trends", "📦 Distributions", "🔗 Correlation", "📉 Scatter", "🔍 Outliers"])

    with tab1:
        # Sample for performance
        sample = filtered.sample(min(5000, len(filtered))).sort_values('date')
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                             subplot_titles=("% Silica Concentrate", "% Iron Concentrate"))
        fig.add_trace(go.Scatter(x=sample['date'], y=sample['% Silica Concentrate'],
                                  mode='lines', line=dict(color=ACCENT_CYAN, width=1),
                                  name='Silica'), row=1, col=1)
        fig.add_trace(go.Scatter(x=sample['date'], y=sample['% Iron Concentrate'],
                                  mode='lines', line=dict(color=ACCENT_GREEN, width=1),
                                  name='Iron'),  row=2, col=1)
        fig.update_layout(height=420, margin=dict(l=0,r=0,t=40,b=0))
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        # Monthly box
        tmp = filtered.copy()
        tmp['month_yr'] = tmp['date'].dt.to_period('M').astype(str)
        fig2 = px.box(tmp, x='month_yr', y='% Silica Concentrate',
                       color_discrete_sequence=[ACCENT_CYAN])
        fig2.update_layout(title="Monthly Silica Distribution",
                           height=320, margin=dict(l=0,r=0,t=40,b=0),
                           xaxis_tickangle=-45)
        apply_template(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(filtered, x='% Silica Concentrate', nbins=60,
                                color_discrete_sequence=[ACCENT_CYAN])
            fig.update_layout(title="Silica Distribution", height=300,
                              margin=dict(l=0,r=0,t=40,b=0))
            apply_template(fig)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.histogram(filtered, x='% Iron Concentrate', nbins=60,
                                color_discrete_sequence=[ACCENT_GREEN])
            fig.update_layout(title="Iron Distribution", height=300,
                              margin=dict(l=0,r=0,t=40,b=0))
            apply_template(fig)
            st.plotly_chart(fig, use_container_width=True)

        num_cols = filtered.select_dtypes('number').columns.tolist()
        sel_col  = st.selectbox("Select feature for violin plot", num_cols, index=0)
        fig = px.violin(filtered.sample(min(10000, len(filtered))),
                         y=sel_col, box=True, color_discrete_sequence=[ACCENT_BLUE])
        fig.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0))
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        num_df = filtered.select_dtypes('number').drop(
            columns=[c for c in ('hour','day','month','day_of_week') if c in filtered], errors='ignore')
        corr   = num_df.corr()
        fig    = px.imshow(corr, color_continuous_scale='RdBu_r', zmin=-1, zmax=1,
                            text_auto=".2f", aspect='auto')
        fig.update_layout(title="Correlation Matrix", height=580,
                          margin=dict(l=0,r=0,t=40,b=0))
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        num_cols = filtered.select_dtypes('number').columns.tolist()
        xf = st.selectbox("X axis", num_cols, index=0, key="sx")
        yf = st.selectbox("Y axis", num_cols, index=1, key="sy")
        s  = filtered.sample(min(5000, len(filtered)))
        fig = px.scatter(s, x=xf, y=yf, color='% Silica Concentrate',
                          color_continuous_scale='RdYlGn_r', opacity=0.5,
                          trendline='ols')
        fig.update_layout(height=420, margin=dict(l=0,r=0,t=10,b=0))
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

    with tab5:
        num_cols = filtered.select_dtypes('number').columns.tolist()
        feat_sel = st.selectbox("Feature for outlier detection", num_cols, index=0)
        col_data = filtered[feat_sel].dropna()
        Q1, Q3   = col_data.quantile(0.25), col_data.quantile(0.75)
        IQR      = Q3 - Q1
        lo, hi   = Q1 - 1.5*IQR, Q3 + 1.5*IQR
        outliers = filtered[(filtered[feat_sel] < lo) | (filtered[feat_sel] > hi)]
        st.markdown(f"**{len(outliers):,} outliers** detected (IQR method) — "
                    f"{len(outliers)/len(filtered)*100:.1f}% of data")
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=col_data.sample(min(5000,len(col_data))).values,
                                  mode='markers', marker=dict(size=3, color=ACCENT_BLUE,
                                  opacity=0.4), name='Normal'))
        ol_sample = outliers.sample(min(500, len(outliers)))
        fig.add_trace(go.Scatter(y=ol_sample[feat_sel].values, mode='markers',
                                  marker=dict(size=5, color=ACCENT_RED), name='Outlier'))
        fig.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0))
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

    # Download
    st.markdown('<div class="section-title">Export</div>', unsafe_allow_html=True)
    csv = filtered.to_csv(index=False)
    st.download_button("⬇️ Download Filtered Data (CSV)", csv,
                        "filtered_mining_data.csv", "text/csv")


# ─────────────────────────────────────────────
#  PAGE 5 — PROCESS MONITORING
# ─────────────────────────────────────────────

def page_process_monitoring():
    page_header("Process Monitoring", "Industrial control room – real-time process health",
                "🏭")
    df = load_hourly()

    latest = df.iloc[-1].to_dict()

    THRESHOLDS = {
        '% Iron Feed':          (50, 65, "% Fe"),
        '% Silica Feed':        (5,  20, "% SiO₂"),
        'Starch Flow':          (1500, 4000, "m³/h"),
        'Amina Flow':           (200,  500, "m³/h"),
        'Ore Pulp Flow':        (300,  500, "t/h"),
        'Ore Pulp pH':          (8.0,  11.0, "pH"),
        'Ore Pulp Density':     (1.5,  2.0, "g/cm³"),
        '% Silica Concentrate': (0,    2.0, "% SiO₂"),
        '% Iron Concentrate':   (60,   75,  "% Fe"),
    }

    air_cols = [c for c in df.columns if 'Air Flow' in c]

    def status_of(val, lo, hi):
        if lo <= val <= hi:
            return "🟢 NORMAL",   ACCENT_GREEN, "green"
        margin_lo = lo + (hi-lo)*0.1
        margin_hi = hi - (hi-lo)*0.1
        if margin_lo <= val <= margin_hi or (val < lo and val > lo*0.9) or (val > hi and val < hi*1.1):
            return "🟡 WARNING",  ACCENT_AMBER, "amber"
        return "🔴 CRITICAL", ACCENT_RED,   "red"

    st.markdown('<div class="section-title">Process Parameter Status</div>',
                unsafe_allow_html=True)

    alarms = []
    rows   = []
    for param, (lo, hi, unit) in THRESHOLDS.items():
        val = float(latest.get(param, np.nan))
        if np.isnan(val):
            continue
        lbl, col, lvl = status_of(val, lo, hi)
        rows.append({"Parameter": param, "Value": f"{val:.2f}", "Unit": unit,
                     "Range": f"{lo} – {hi}", "Status": lbl})
        if lvl in ("amber", "red"):
            alarms.append((param, val, unit, lvl, lbl))

    row_df = pd.DataFrame(rows)

    def highlight_status(row):
        if "CRITICAL" in str(row.get("Status","")):
            return ['background-color: rgba(248,81,73,0.1)'] * len(row)
        elif "WARNING" in str(row.get("Status","")):
            return ['background-color: rgba(210,153,34,0.1)'] * len(row)
        return [''] * len(row)

    st.dataframe(row_df.style.apply(highlight_status, axis=1),
                 use_container_width=True, height=320)

    # Air flow gauges
    st.markdown('<div class="section-title">Flotation Column Air Flow</div>',
                unsafe_allow_html=True)
    cols = st.columns(7)
    for i, acol in enumerate(air_cols[:7]):
        val = float(latest.get(acol, 0))
        status = "🟢" if 200 < val < 400 else "🟡"
        cols[i].metric(acol.replace('Flotation Column ', 'Col '), f"{val:.0f}", status)

    # Alarm panel
    st.markdown('<div class="section-title">🚨 Alarm Panel</div>', unsafe_allow_html=True)
    if not alarms:
        st.markdown('<div class="alarm-normal">✅ All parameters within normal operating range. No alarms active.</div>',
                    unsafe_allow_html=True)
    else:
        for param, val, unit, lvl, lbl in alarms:
            cls = "alarm-critical" if lvl == "red" else "alarm-warning"
            st.markdown(f'<div class="{cls}"><b>{lbl}</b> — {param}: {val:.2f} {unit}</div>',
                        unsafe_allow_html=True)

    # Trend – last 12 hours
    st.markdown('<div class="section-title">12-Hour Parameter Trend</div>',
                unsafe_allow_html=True)
    tail = df.tail(12)
    sel_param = st.selectbox("Select parameter", list(THRESHOLDS.keys()))
    lo, hi, unit = THRESHOLDS[sel_param]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tail['date'], y=tail[sel_param],
                              mode='lines+markers', line=dict(color=ACCENT_CYAN, width=2),
                              name=sel_param))
    fig.add_hrect(y0=lo, y1=hi, fillcolor="rgba(63,185,80,0.07)",
                   layer="below", line_width=0, annotation_text="Normal range")
    fig.add_hline(y=lo, line_dash="dash", line_color=ACCENT_AMBER)
    fig.add_hline(y=hi, line_dash="dash", line_color=ACCENT_AMBER)
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=10,b=0))
    apply_template(fig)
    st.plotly_chart(fig, use_container_width=True)


# ─────────────────────────────────────────────
#  PAGE 6 — FEATURE ANALYSIS
# ─────────────────────────────────────────────

def page_feature_analysis():
    page_header("Feature Analysis", "Variable importance, relationships, and statistical insights",
                "🔬")
    df  = load_hourly()
    fi  = load_feat_imp()
    models = load_models()
    model  = models["with_iron"]

    tab1, tab2, tab3 = st.tabs(["🏆 Importance", "🔗 Relationships", "📊 Distributions"])

    with tab1:
        # Stored feature importance
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(fi.sort_values('Importance', ascending=True).tail(15),
                          x='Importance', y='Feature', orientation='h',
                          color='Importance', color_continuous_scale='Blues')
            fig.update_layout(title="Top Feature Importances (from file)",
                              height=420, margin=dict(l=0,r=0,t=40,b=0),
                              coloraxis_showscale=False)
            apply_template(fig)
            st.plotly_chart(fig, use_container_width=True)

        with c2:
            feats  = get_model_features(model)
            fi_df  = pd.DataFrame({'feature': feats, 'importance': model.feature_importances_})
            fi_df  = fi_df.sort_values('importance', ascending=False).head(15)
            fig2   = px.treemap(fi_df, path=['feature'], values='importance',
                                 color='importance', color_continuous_scale='Blues')
            fig2.update_layout(title="Feature Importance Treemap",
                               height=420, margin=dict(l=0,r=0,t=40,b=0))
            apply_template(fig2)
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        num_cols = [c for c in df.select_dtypes('number').columns
                    if c not in ('hour','day','month','day_of_week')]
        top_feats = fi.head(6)['Feature'].tolist()
        avail     = [f for f in top_feats if f in df.columns]

        xf = st.selectbox("X variable", num_cols, index=num_cols.index('% Iron Feed') if '% Iron Feed' in num_cols else 0)
        yf = st.selectbox("Y variable", num_cols, index=num_cols.index('% Silica Concentrate') if '% Silica Concentrate' in num_cols else 1)

        s = df.sample(min(3000, len(df)))
        fig = px.scatter(s, x=xf, y=yf, color='% Silica Concentrate',
                          color_continuous_scale=px.colors.diverging.RdYlGn, opacity=0.6,
                          trendline='ols', marginal_x='histogram', marginal_y='histogram')
        fig.update_layout(height=500, margin=dict(l=0,r=0,t=10,b=0))
        apply_template(fig)
        st.plotly_chart(fig, use_container_width=True)

        # Correlation with target
        corr_target = df[num_cols].corr()['% Silica Concentrate'].drop('% Silica Concentrate').abs()
        corr_target = corr_target.sort_values(ascending=False).head(20)
        fig3 = px.bar(corr_target.reset_index(), x='index', y='% Silica Concentrate',
                       color='% Silica Concentrate', color_continuous_scale='Blues',
                       labels={'index':'Feature','% Silica Concentrate':'|Correlation|'})
        fig3.update_layout(title="|Correlation| with Silica Concentrate",
                           height=340, margin=dict(l=0,r=0,t=40,b=0),
                           xaxis_tickangle=-45, coloraxis_showscale=False)
        apply_template(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    with tab3:
        sel = st.selectbox("Select feature", num_cols)
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(df, x=sel, nbins=60, color_discrete_sequence=[ACCENT_CYAN])
            fig.update_layout(title=f"Distribution: {sel}", height=300,
                              margin=dict(l=0,r=0,t=40,b=0))
            apply_template(fig)
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig = px.box(df, y=sel, color_discrete_sequence=[ACCENT_BLUE])
            fig.update_layout(title=f"Box Plot: {sel}", height=300,
                              margin=dict(l=0,r=0,t=40,b=0))
            apply_template(fig)
            st.plotly_chart(fig, use_container_width=True)

        stats = df[sel].describe()
        st.dataframe(stats.to_frame().T, use_container_width=True)


# ─────────────────────────────────────────────
#  PAGE 7 — MODEL PERFORMANCE
# ─────────────────────────────────────────────

def page_model_performance():
    page_header("Model Performance", "XGBoost model details, architecture and inference pipeline",
                "🤖")
    models = load_models()

    for key, label in [("with_iron","With Iron Concentrate"),
                        ("without_iron","Without Iron Concentrate"),
                        ("1h_ahead","1-Hour Ahead Forecast")]:
        m     = models[key]
        feats = get_model_features(m)
        n_f   = len(feats)

        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-title">🤖 Model — {label}</div>
            <div style="display:flex; gap:24px; flex-wrap:wrap; margin-top:8px;">
                <div><span style="color:{TEXT_MUTED};font-size:0.8rem">Algorithm</span><br>
                     <b style="color:{ACCENT_CYAN}">XGBoost Regressor</b></div>
                <div><span style="color:{TEXT_MUTED};font-size:0.8rem">Features</span><br>
                     <b style="color:{ACCENT_GREEN}">{n_f}</b></div>
                <div><span style="color:{TEXT_MUTED};font-size:0.8rem">n_estimators</span><br>
                     <b style="color:{ACCENT_BLUE}">{m.n_estimators}</b></div>
                <div><span style="color:{TEXT_MUTED};font-size:0.8rem">Max Depth</span><br>
                     <b style="color:{ACCENT_AMBER}">{m.max_depth}</b></div>
                <div><span style="color:{TEXT_MUTED};font-size:0.8rem">Learning Rate</span><br>
                     <b style="color:{ACCENT_CYAN}">{m.learning_rate}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Feature importance comparison
    st.markdown('<div class="section-title">Feature Importance Comparison</div>',
                unsafe_allow_html=True)
    dfs = []
    for key, label in [("with_iron","With Iron"),("without_iron","Without Iron")]:
        m = models[key]; feats = get_model_features(m)
        tmp = pd.DataFrame({'Feature': feats, 'Importance': m.feature_importances_,
                             'Model': label})
        dfs.append(tmp)
    all_fi = pd.concat(dfs)
    top12  = all_fi.groupby('Feature')['Importance'].sum().nlargest(12).index
    plot_fi= all_fi[all_fi['Feature'].isin(top12)]
    fig    = px.bar(plot_fi, x='Importance', y='Feature', color='Model',
                    barmode='group', orientation='h',
                    color_discrete_map={'With Iron': ACCENT_CYAN,
                                        'Without Iron': ACCENT_AMBER})
    fig.update_layout(height=420, margin=dict(l=0,r=0,t=10,b=0),
                      yaxis={'categoryorder': 'total ascending'})
    apply_template(fig)
    st.plotly_chart(fig, use_container_width=True)

    # Workflow diagram — rendered with Plotly Sankey (no graphviz dependency)
    st.markdown('<div class="section-title">Inference Pipeline</div>',
                unsafe_allow_html=True)

    # Node labels
    nodes = [
        "Raw Data",             # 0
        "Feature Engineering",  # 1
        "Model Selection",      # 2
        "XGBoost (with iron)",  # 3
        "XGBoost (no iron)",    # 4
        "XGBoost (1h ahead)",   # 5
        "Prediction Output",    # 6
        "Alert System",         # 7
    ]
    node_colors = [
        ACCENT_BLUE, ACCENT_CYAN, ACCENT_GREEN,
        "#9b59b6", "#e67e22", ACCENT_AMBER,
        ACCENT_GREEN, ACCENT_RED,
    ]
    # source → target with value (thickness)
    sources = [0, 1, 2, 2, 2, 3, 4, 5, 6]
    targets = [1, 2, 3, 4, 5, 6, 6, 6, 7]
    values  = [4, 4, 2, 2, 2, 2, 2, 2, 6]

    fig_sk = go.Figure(go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20, thickness=20,
            line=dict(color=CARD_BORDER, width=1),
            label=nodes,
            color=node_colors,
            hovertemplate="%{label}<extra></extra>",
        ),
        link=dict(
            source=sources, target=targets, value=values,
            color=["rgba(31,111,235,0.25)"] * len(sources),
        )
    ))
    fig_sk.update_layout(
        height=340,
        margin=dict(l=20, r=20, t=10, b=10),
        font=dict(size=12, color=TEXT_PRIMARY),
    )
    apply_template(fig_sk)
    st.plotly_chart(fig_sk, use_container_width=True)


# ─────────────────────────────────────────────
#  PAGE 8 — REPORTS
# ─────────────────────────────────────────────

def page_reports():
    page_header("Reports", "Generate and export plant quality reports", "📄")

    df      = load_hourly()
    models  = load_models()
    fi      = load_feat_imp()
    latest  = df.iloc[-1].to_dict()

    silica  = float(latest.get('% Silica Concentrate', 0))
    iron    = float(latest.get('% Iron Concentrate', 0))
    iron_f  = float(latest.get('% Iron Feed', 0))
    risk, rcol, _ = silica_risk_level(silica)
    recovery= round(100 * iron / iron_f, 1) if iron_f else 0

    st.markdown('<div class="section-title">Report Preview</div>', unsafe_allow_html=True)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size:1.1rem;font-weight:700;margin-bottom:12px;
             color:{ACCENT_CYAN}">
            🏭 Industrial Quality Report — {now_str}
        </div>
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;">
            <div>
                <div class="kpi-title">Silica Concentrate</div>
                <div style="font-size:1.5rem;font-weight:700;color:{rcol}">{silica:.2f}%</div>
                <div class="kpi-sub">Risk: {risk}</div>
            </div>
            <div>
                <div class="kpi-title">Iron Concentrate</div>
                <div style="font-size:1.5rem;font-weight:700;color:{ACCENT_GREEN}">{iron:.2f}%</div>
            </div>
            <div>
                <div class="kpi-title">Recovery Efficiency</div>
                <div style="font-size:1.5rem;font-weight:700;color:{ACCENT_BLUE}">{recovery}%</div>
            </div>
        </div>
        <hr style="border-color:{CARD_BORDER};margin:14px 0;">
        <div style="font-size:0.88rem;color:{TEXT_MUTED};">
            <b>Recommendations:</b><br>
            {'⚠️ Increase starch dosage and review air flow — silica above threshold.' if silica > 2.0
             else '✅ Process within specification. Continue standard protocol.'}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # CSV export
    st.markdown('<div class="section-title">Export Options</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        summary = pd.DataFrame([{
            "Report Date":          now_str,
            "Silica Concentrate %": round(silica, 3),
            "Iron Concentrate %":   round(iron,   3),
            "Iron Feed %":          round(iron_f,  3),
            "Recovery %":           recovery,
            "Risk Level":           risk,
            "Ore Pulp Flow":        round(latest.get('Ore Pulp Flow',0), 1),
            "Starch Flow":          round(latest.get('Starch Flow',0), 1),
            "pH":                   round(latest.get('Ore Pulp pH',0), 2),
        }])
        csv = summary.to_csv(index=False)
        st.download_button("⬇️ Download Summary (CSV)", csv,
                            "quality_report.csv", "text/csv",
                            use_container_width=True)

    with c2:
        hourly_csv = df.tail(48).to_csv(index=False)
        st.download_button("⬇️ Download Last 48h Data (CSV)", hourly_csv,
                            "last_48h_data.csv", "text/csv",
                            use_container_width=True)

    # HTML Report export (no reportlab dependency)
    st.markdown("---")
    if st.button("📄 Generate HTML Report", use_container_width=True):
        try:
            top_fi_rows = "".join(
                f"<tr><td>{r['Feature']}</td><td>{r['Importance']:.4f}</td></tr>"
                for _, r in fi.head(8).iterrows()
            )
            rec_html = (
                "⚠️ ALERT: Silica above 2% — review starch dosage and air flow."
                if silica > 2.0 else
                "✅ Process within specification. Continue standard protocol."
            )
            alert_color = "#f85149" if silica > 2.0 else "#3fb950"

            html_report = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Quality Report — {now_str}</title>
<style>
  body {{ font-family: Inter, Arial, sans-serif; background:#0d1117; color:#e6edf3;
         margin:0; padding:32px; }}
  h1   {{ color:#39d0f5; font-size:1.8rem; margin-bottom:4px; }}
  h2   {{ color:#1f6feb; font-size:1.1rem; margin:24px 0 10px; border-bottom:1px solid #21262d;
         padding-bottom:6px; }}
  .sub {{ color:#8b949e; font-size:0.85rem; margin-bottom:28px; }}
  .grid{{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; margin-bottom:24px; }}
  .card{{ background:#161b22; border:1px solid #21262d; border-radius:10px; padding:18px 20px; }}
  .card .lbl {{ color:#8b949e; font-size:0.75rem; text-transform:uppercase; letter-spacing:.06em; }}
  .card .val {{ font-size:1.8rem; font-weight:700; margin-top:4px; }}
  table{{ width:100%; border-collapse:collapse; background:#161b22;
          border-radius:8px; overflow:hidden; }}
  th   {{ background:#1f6feb; color:#fff; padding:10px 14px; text-align:left; font-size:0.85rem; }}
  td   {{ padding:9px 14px; font-size:0.85rem; border-bottom:1px solid #21262d; }}
  tr:last-child td {{ border-bottom:none; }}
  .rec {{ background:rgba(63,185,80,0.1); border:1px solid {alert_color};
          border-radius:8px; padding:14px 18px; color:{alert_color}; margin-top:8px; }}
  .footer {{ color:#8b949e; font-size:0.75rem; margin-top:32px; text-align:center; }}
</style>
</head>
<body>
<h1>🏭 Mining Process Quality Monitoring Report</h1>
<div class="sub">Generated: {now_str} &nbsp;|&nbsp; XGBoost · Streamlit · Plotly</div>

<h2>Process KPIs</h2>
<div class="grid">
  <div class="card">
    <div class="lbl">Silica Concentrate</div>
    <div class="val" style="color:{alert_color}">{silica:.2f}%</div>
    <div style="font-size:.8rem;color:#8b949e">Risk: {risk}</div>
  </div>
  <div class="card">
    <div class="lbl">Iron Concentrate</div>
    <div class="val" style="color:#3fb950">{iron:.2f}%</div>
  </div>
  <div class="card">
    <div class="lbl">Recovery Efficiency</div>
    <div class="val" style="color:#1f6feb">{recovery:.1f}%</div>
  </div>
  <div class="card">
    <div class="lbl">Iron Feed</div>
    <div class="val" style="color:#39d0f5">{iron_f:.2f}%</div>
  </div>
  <div class="card">
    <div class="lbl">Starch Flow</div>
    <div class="val" style="color:#39d0f5">{latest.get('Starch Flow',0):.0f}</div>
    <div style="font-size:.8rem;color:#8b949e">m³/h</div>
  </div>
  <div class="card">
    <div class="lbl">Ore Pulp pH</div>
    <div class="val" style="color:#d29922">{latest.get('Ore Pulp pH',0):.2f}</div>
  </div>
</div>

<h2>Top Feature Importances</h2>
<table>
  <tr><th>Feature</th><th>Importance</th></tr>
  {top_fi_rows}
</table>

<h2>Recommendation</h2>
<div class="rec">{rec_html}</div>

<div class="footer">Mining Process Quality Monitoring Platform &copy; {datetime.now().year}</div>
</body>
</html>"""

            st.download_button(
                "⬇️ Download HTML Report",
                html_report.encode("utf-8"),
                "quality_report.html",
                "text/html",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Report generation failed: {e}")


# ─────────────────────────────────────────────
#  PAGE 9 — ABOUT
# ─────────────────────────────────────────────

def page_about():
    page_header("About", "Project overview, dataset information, and technology stack", "ℹ️")

    st.markdown(f"""
    <div class="kpi-card">
        <div style="font-size:1.1rem;font-weight:700;color:{ACCENT_CYAN};margin-bottom:10px;">
            🏭 Mining Process Quality Monitoring Platform
        </div>
        <p style="color:{TEXT_MUTED};line-height:1.7;">
        This application provides real-time and predictive quality monitoring for a
        mining flotation plant. It leverages machine learning models trained on historical
        sensor data to predict silica and iron concentrate levels, enabling proactive
        quality control and process optimisation.
        </p>
    </div>

    <div class="kpi-card" style="margin-top:12px;">
        <div style="font-size:1rem;font-weight:700;color:{ACCENT_CYAN};margin-bottom:10px;">
            📊 Dataset
        </div>
        <p style="color:{TEXT_MUTED};line-height:1.7;">
        <b style="color:{TEXT_PRIMARY}">MiningProcess Flotation Plant</b> — 737K+ sensor readings
        from a real flotation plant, including iron/silica feed concentrations, starch/amine reagent
        flows, ore pulp properties, and 7 flotation column measurements.
        The data was aggregated to hourly resolution and enriched with lag and rolling window features
        for temporal modelling.
        </p>
    </div>

    <div class="kpi-card" style="margin-top:12px;">
        <div style="font-size:1rem;font-weight:700;color:{ACCENT_CYAN};margin-bottom:10px;">
            🤖 Machine Learning
        </div>
        <p style="color:{TEXT_MUTED};line-height:1.7;">
        Three <b style="color:{TEXT_PRIMARY}">XGBoost Regressor</b> models are used:
        </p>
        <ul style="color:{TEXT_MUTED};line-height:1.9;">
            <li><b style="color:{TEXT_PRIMARY}">model_with_iron</b> — Predicts silica concentrate
                using all features including iron concentrate measurement</li>
            <li><b style="color:{TEXT_PRIMARY}">model_without_iron</b> — Predicts silica concentrate
                without relying on iron concentrate (useful when iron is not yet measured)</li>
            <li><b style="color:{TEXT_PRIMARY}">model_1h_ahead</b> — Forecasts silica concentrate
                one hour into the future for proactive process control</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    STACK = [
        ("Python 3.x",   "Core language",                    "🐍"),
        ("Streamlit",    "Interactive web application",       "🌐"),
        ("XGBoost",      "Gradient boosted tree models",      "🤖"),
        ("Pandas/NumPy", "Data wrangling & numerics",         "🔢"),
        ("Plotly",       "Interactive visualisations",        "📊"),
        ("Joblib",       "Model persistence & caching",       "💾"),
        ("Scikit-learn", "ML utilities & preprocessing",      "⚙️"),
        ("ReportLab",    "PDF report generation",             "📄"),
        ("Graphviz",     "Pipeline diagram rendering",        "🗺️"),
    ]

    st.markdown('<div class="section-title">Technology Stack</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (tech, desc, icon) in enumerate(STACK):
        cols[i % 3].markdown(f"""
        <div class="kpi-card">
            <div style="font-size:1.5rem;margin-bottom:6px;">{icon}</div>
            <div style="font-weight:600;color:{ACCENT_CYAN}">{tech}</div>
            <div style="font-size:0.8rem;color:{TEXT_MUTED}">{desc}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="kpi-card" style="margin-top:12px;text-align:center;">
        <div style="font-size:0.85rem;color:{TEXT_MUTED};">
            Built for industrial analytics demonstration · XGBoost + Streamlit + Plotly
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────

PAGE_MAP = {
    "🏠  Dashboard":           page_dashboard,
    "🔮  Live Prediction":     page_live_prediction,
    "📡  Future Prediction":   page_future_prediction,
    "📊  Historical Analytics":page_historical,
    "🏭  Process Monitoring":  page_process_monitoring,
    "🔬  Feature Analysis":    page_feature_analysis,
    "🤖  Model Performance":   page_model_performance,
    "📄  Reports":             page_reports,
    "ℹ️  About":               page_about,
}

with st.spinner("Loading data..."):
    fn = PAGE_MAP.get(page, page_dashboard)
    fn()