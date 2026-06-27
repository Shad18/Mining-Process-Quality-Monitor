import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Industrial Quality Monitoring Platform",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# AUTO-REFRESH  (must be before any widget)
# ─────────────────────────────────────────────
if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False
if "refresh_interval" not in st.session_state:
    st.session_state.refresh_interval = 10
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
if "page" not in st.session_state:
    st.session_state.page = "📊  Dashboard"

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

:root {
  --bg-primary:    #0a0d12;
  --bg-secondary:  #10151e;
  --bg-card:       #141b27;
  --bg-card-alt:   #1a2235;
  --border:        #1f2d44;
  --border-glow:   rgba(0,212,255,0.2);
  --accent-cyan:   #00d4ff;
  --accent-green:  #00ff88;
  --accent-amber:  #ffaa00;
  --accent-red:    #ff3355;
  --accent-purple: #a855f7;
  --text-primary:  #e8edf5;
  --text-secondary:#8899b3;
  --text-dim:      #4a5a72;
  --font-display:  'Rajdhani', sans-serif;
  --font-mono:     'Share Tech Mono', monospace;
  --font-body:     'Inter', sans-serif;
}

html, body, [class*="css"], [data-testid="stAppViewContainer"] {
  background-color: var(--bg-primary) !important;
  color: var(--text-primary) !important;
  font-family: var(--font-body);
}
[data-testid="stAppViewContainer"] > .main { background-color: var(--bg-primary) !important; }
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

[data-testid="stSidebar"] {
  background: var(--bg-secondary) !important;
  border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"] * { color: var(--text-primary) !important; }
[data-testid="stSidebar"] .stRadio label {
  background: var(--bg-card) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  padding: 10px 14px !important;
  margin: 3px 0 !important;
  display: block; cursor: pointer;
  font-family: var(--font-display); font-weight: 600; letter-spacing: 0.5px;
  transition: all 0.2s ease;
}
[data-testid="stSidebar"] .stRadio label:hover {
  border-color: var(--accent-cyan) !important;
  background: var(--bg-card-alt) !important;
}

h1, h2, h3 { font-family: var(--font-display) !important; font-weight: 700 !important; }

/* KPI CARDS */
.kpi-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 20px; }
.kpi-card {
  background: var(--bg-card);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 18px 20px 14px 20px;
  position: relative; overflow: hidden;
  transition: all 0.25s ease;
  min-width: 0;
}
.kpi-card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
  background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
}
.kpi-card:hover { border-color: var(--accent-cyan); transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,212,255,0.1); }
.kpi-top { display: flex; justify-content: space-between; align-items: flex-start; }
.kpi-label { font-size: 10px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; color: var(--text-secondary); margin-bottom: 10px; }
.kpi-value { font-family: var(--font-mono); font-size: 28px; font-weight: 700; line-height: 1; margin-bottom: 8px; }
.kpi-unit { font-size: 13px; color: var(--text-dim); margin-left: 3px; }
.kpi-icon { font-size: 22px; opacity: 0.2; margin-top: 2px; }
.kpi-delta { font-size: 11px; font-weight: 500; display: flex; align-items: center; gap: 4px; }
.delta-up   { color: #00ff88; }
.delta-down { color: #ff3355; }
.kpi-bar { height: 3px; border-radius: 2px; margin-top: 10px; background: var(--border); overflow: hidden; }
.kpi-bar-fill { height: 100%; border-radius: 2px; transition: width 0.4s ease; }

/* BADGES */
.badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 11px; font-weight: 600; letter-spacing: 0.8px; text-transform: uppercase; font-family: var(--font-mono); }
.badge-green  { background: rgba(0,255,136,0.1); color: #00ff88; border: 1px solid rgba(0,255,136,0.25); }
.badge-amber  { background: rgba(255,170,0,0.1); color: #ffaa00; border: 1px solid rgba(255,170,0,0.25); }
.badge-red    { background: rgba(255,51,85,0.1);  color: #ff3355; border: 1px solid rgba(255,51,85,0.25); }
.badge-cyan   { background: rgba(0,212,255,0.1);  color: #00d4ff; border: 1px solid rgba(0,212,255,0.25); }

/* ALERT BANNERS */
.alert-critical { background: rgba(255,51,85,0.07); border: 1px solid rgba(255,51,85,0.25); border-left: 4px solid #ff3355; border-radius: 8px; padding: 12px 16px; margin: 5px 0; font-family: var(--font-display); font-weight: 600; font-size: 14px; }
.alert-warning  { background: rgba(255,170,0,0.07); border: 1px solid rgba(255,170,0,0.25); border-left: 4px solid #ffaa00; border-radius: 8px; padding: 12px 16px; margin: 5px 0; font-family: var(--font-display); font-weight: 600; font-size: 14px; }
.alert-ok       { background: rgba(0,255,136,0.07); border: 1px solid rgba(0,255,136,0.25); border-left: 4px solid #00ff88; border-radius: 8px; padding: 12px 16px; margin: 5px 0; font-family: var(--font-display); font-weight: 600; font-size: 14px; }

/* SECTION TITLE */
.section-title { font-family: var(--font-display); font-size: 12px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: var(--text-secondary); border-bottom: 1px solid var(--border); padding-bottom: 8px; margin: 22px 0 14px 0; display: flex; align-items: center; gap: 8px; }
.section-title::before { content: ''; display: inline-block; width: 3px; height: 13px; background: var(--accent-cyan); border-radius: 2px; }

/* TABLE */
.event-table { width: 100%; border-collapse: collapse; font-family: var(--font-body); font-size: 13px; }
.event-table th { background: var(--bg-card-alt); color: var(--text-secondary); padding: 10px 14px; text-align: left; font-size: 10px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; border-bottom: 1px solid var(--border); }
.event-table td { padding: 10px 14px; border-bottom: 1px solid var(--border); color: var(--text-primary); }
.event-table tr:hover td { background: var(--bg-card-alt); }
.event-table tr:last-child td { border-bottom: none; }

/* TIMESTAMP */
.timestamp { font-family: var(--font-mono); font-size: 12px; color: var(--accent-cyan); background: rgba(0,212,255,0.05); padding: 4px 10px; border-radius: 4px; border: 1px solid var(--border-glow); }

/* LIVE DOT */
.live-dot { display: inline-block; width: 8px; height: 8px; background: var(--accent-green); border-radius: 50%; margin-right: 6px; animation: pulse-dot 2s infinite; }
@keyframes pulse-dot { 0% { box-shadow: 0 0 0 0 rgba(0,255,136,0.4); } 70% { box-shadow: 0 0 0 8px rgba(0,255,136,0); } 100% { box-shadow: 0 0 0 0 rgba(0,255,136,0); } }

/* HERO BANNER */
.hero-banner { background: linear-gradient(135deg, #141b27 0%, #0f1829 100%); border: 1px solid var(--border); border-radius: 12px; padding: 26px 30px; margin-bottom: 22px; position: relative; overflow: hidden; }
.hero-banner::after { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(255,255,255,0.012) 2px, rgba(255,255,255,0.012) 4px); pointer-events: none; }
.hero-title { font-family: var(--font-display); font-size: 32px; font-weight: 700; letter-spacing: 2px; background: linear-gradient(90deg, #00d4ff, #a855f7, #00ff88); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0 0 5px 0; }
.hero-sub { font-family: var(--font-mono); font-size: 12px; color: var(--text-secondary); letter-spacing: 1px; }

/* LOGO */
.logo-container { display: flex; align-items: center; gap: 12px; padding: 6px 0 18px 0; border-bottom: 1px solid var(--border); margin-bottom: 18px; }
.logo-icon { width: 42px; height: 42px; background: linear-gradient(135deg, #00d4ff, #a855f7); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
.logo-text-main { font-family: var(--font-display); font-size: 16px; font-weight: 700; color: var(--text-primary); line-height: 1.2; }
.logo-text-sub  { font-family: var(--font-mono); font-size: 9px; color: var(--accent-cyan); letter-spacing: 2px; text-transform: uppercase; }
.nav-label { font-family: var(--font-mono); font-size: 10px; letter-spacing: 2px; text-transform: uppercase; color: var(--text-dim); margin: 14px 0 6px 0; }

/* MACHINE CARD */
.machine-card { background: var(--bg-card); border: 1px solid var(--border); border-radius: 10px; padding: 16px; margin-bottom: 12px; transition: all 0.2s; }
.machine-card:hover { transform: translateY(-1px); }

hr { border-color: var(--border) !important; }
.stSelectbox > div > div, .stMultiSelect > div > div { background: var(--bg-card) !important; border: 1px solid var(--border) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PLOTLY CONSTANTS
# ─────────────────────────────────────────────
PLOT_BG  = "#141b27"
PAPER_BG = "#141b27"
GRID_CLR = "#1f2d44"
TEXT_CLR = "#8899b3"
FONT_FAM = "Rajdhani, Inter, sans-serif"

def base_layout(title="", height=340):
    return dict(
        title=dict(text=title, font=dict(family=FONT_FAM, size=14, color="#e8edf5"), x=0.01),
        plot_bgcolor=PLOT_BG, paper_bgcolor=PAPER_BG,
        font=dict(family=FONT_FAM, color=TEXT_CLR),
        height=height, margin=dict(l=44, r=20, t=48, b=40),
        xaxis=dict(gridcolor=GRID_CLR, linecolor=GRID_CLR, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=GRID_CLR, linecolor=GRID_CLR, tickfont=dict(size=11)),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=11)),
        hovermode="x unified",
    )

# ─────────────────────────────────────────────
# DATA GENERATORS  (no cache → live on refresh)
# ─────────────────────────────────────────────
def generate_time_series(hours=24, points=288):
    rng = np.random.default_rng(int(time.time() // 5))   # changes every 5 s
    now = datetime.now()
    times = [now - timedelta(hours=hours) + timedelta(minutes=i*(hours*60//points)) for i in range(points)]
    quality    = np.clip(87 + np.cumsum(rng.normal(0, 0.3, points)) + 5*np.sin(np.linspace(0, 6*np.pi, points)), 65, 99)
    temp       = 72 + 8*np.sin(np.linspace(0, 4*np.pi, points)) + rng.normal(0, 1.5, points)
    pressure   = 1013 + 20*np.sin(np.linspace(0, 3*np.pi, points)) + rng.normal(0, 3, points)
    vibration  = np.abs(rng.normal(2.4, 0.6, points))
    defect_rate= np.clip(1.5 - 0.008*quality + rng.normal(0, 0.1, points), 0.1, 5.0)
    throughput = 850 + 120*np.sin(np.linspace(0, 2*np.pi, points)) + rng.normal(0, 15, points)
    return pd.DataFrame({"time": times, "quality": quality, "temperature": temp,
                         "pressure": pressure, "vibration": vibration,
                         "defect_rate": defect_rate, "throughput": throughput})

def generate_machine_data():
    rng = np.random.default_rng(int(time.time() // 5))
    machines = [f"UNIT-{i:03d}" for i in range(1, 13)]
    zones = (["Zone A – Assembly"]*3 + ["Zone B – Fabrication"]*3 +
             ["Zone C – Finishing"]*3 + ["Zone D – Packaging"]*3)
    statuses = rng.choice(
        ["OPERATIONAL", "WARNING", "CRITICAL", "IDLE"],
        size=12, p=[0.65, 0.20, 0.10, 0.05]
    )
    return pd.DataFrame({
        "machine": machines, "zone": zones, "status": statuses,
        "quality_score": np.clip(rng.normal(88, 8, 12), 60, 99),
        "oee":           np.clip(rng.normal(82, 10, 12), 55, 97),
        "temperature":   rng.uniform(65, 95, 12),
        "vibration":     rng.uniform(1.2, 5.8, 12),
        "uptime":        rng.uniform(88, 99.5, 12),
    })

def generate_alerts():
    now = datetime.now()
    return pd.DataFrame([
        {"time": now-timedelta(minutes=2),  "severity":"CRITICAL","machine":"UNIT-005","message":"Vibration threshold exceeded — bearing wear suspected"},
        {"time": now-timedelta(minutes=8),  "severity":"WARNING", "machine":"UNIT-003","message":"Temperature rising above 89°C — cooling check advised"},
        {"time": now-timedelta(minutes=15), "severity":"WARNING", "machine":"UNIT-011","message":"Pressure variance ±12% outside normal range"},
        {"time": now-timedelta(minutes=31), "severity":"INFO",    "machine":"UNIT-008","message":"Scheduled maintenance cycle completed successfully"},
        {"time": now-timedelta(minutes=47), "severity":"CRITICAL","machine":"UNIT-005","message":"Quality score dropped below 70% threshold"},
        {"time": now-timedelta(minutes=62), "severity":"INFO",    "machine":"UNIT-001","message":"Production target achieved — 850 units this shift"},
        {"time": now-timedelta(minutes=88), "severity":"WARNING", "machine":"UNIT-009","message":"OEE dropped to 61% — investigate bottleneck"},
        {"time": now-timedelta(minutes=110),"severity":"INFO",    "machine":"UNIT-002","message":"Sensor calibration verified — all readings nominal"},
    ])

def generate_defect_breakdown():
    return pd.DataFrame({
        "category":    ["Surface Finish","Dimensional","Assembly Gap","Contamination","Material Flaw","Calibration Drift"],
        "count":       [142, 98, 67, 43, 31, 18],
        "cost_impact": [28400, 19600, 13400, 8600, 6200, 3600],
    })

def generate_shift_data():
    return pd.DataFrame({
        "shift":   ["Day–Mon","Day–Tue","Day–Wed","Day–Thu","Day–Fri","Day–Sat",
                    "Night–Mon","Night–Tue","Night–Wed","Night–Thu","Night–Fri","Night–Sat"],
        "units":   [847,912,889,934,901,723,798,856,834,878,812,654],
        "defects": [23,18,29,12,21,31,34,27,38,19,28,45],
        "quality": [97.3,98.0,96.7,98.7,97.7,95.7,95.7,96.8,95.4,97.8,96.6,93.1],
        "type":    ["Day"]*6+["Night"]*6,
    })

# ─────────────────────────────────────────────
# CHART BUILDERS
# ─────────────────────────────────────────────
def quality_gauge(value):
    # Use only standard 6-char hex or rgb() — Plotly rejects 8-char hex in gauge
    bar_color = "#00d4ff"
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=round(float(value), 1),
        delta={
            "reference": 85,
            "valueformat": ".1f",
            "increasing": {"color": "rgb(0,255,136)"},
            "decreasing": {"color": "rgb(255,51,85)"},
        },
        title={"text": "Quality Score", "font": {"size": 13, "color": "#8899b3", "family": FONT_FAM}},
        number={"suffix": "%", "font": {"size": 40, "color": "#e8edf5", "family": "Share Tech Mono"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#1f2d44",
                     "tickfont": {"color": "#4a5a72", "size": 10}},
            "bar": {"color": bar_color, "thickness": 0.22},
            "bgcolor": "#1a2235",
            "borderwidth": 0,
            "steps": [
                {"range": [0,  70],  "color": "rgba(255,51,85,0.08)"},
                {"range": [70, 85],  "color": "rgba(255,170,0,0.08)"},
                {"range": [85, 100], "color": "rgba(0,255,136,0.08)"},
            ],
            "threshold": {
                "line": {"color": "#00d4ff", "width": 3},
                "thickness": 0.75,
                "value": float(value),
            },
        }
    ))
    fig.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                      height=230, margin=dict(l=20, r=20, t=56, b=10),
                      font=dict(family=FONT_FAM))
    return fig

def oee_gauge(value):
    if float(value) >= 85:
        color = "rgb(0,255,136)"
    elif float(value) >= 70:
        color = "rgb(255,170,0)"
    else:
        color = "rgb(255,51,85)"
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=round(float(value), 1),
        number={"suffix": "%", "font": {"size": 38, "color": color, "family": "Share Tech Mono"}},
        title={"text": "Overall Equipment Effectiveness", "font": {"size": 12, "color": "#8899b3", "family": FONT_FAM}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#1f2d44",
                     "tickfont": {"color": "#4a5a72", "size": 10}},
            "bar": {"color": color, "thickness": 0.20},
            "bgcolor": "#1a2235",
            "borderwidth": 0,
            "steps": [
                {"range": [0,  65],  "color": "rgba(255,51,85,0.06)"},
                {"range": [65, 85],  "color": "rgba(255,170,0,0.06)"},
                {"range": [85, 100], "color": "rgba(0,255,136,0.06)"},
            ],
        }
    ))
    fig.update_layout(paper_bgcolor=PAPER_BG, height=210,
                      margin=dict(l=20, r=20, t=56, b=10),
                      font=dict(family=FONT_FAM))
    return fig

def quality_trend_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["time"], y=df["quality"], mode="lines", name="Quality %",
                             line=dict(color="#00d4ff", width=2),
                             fill="tozeroy", fillcolor="rgba(0,212,255,0.05)"))
    fig.add_hline(y=85, line_dash="dot", line_color="rgba(255,170,0,0.5)",
                  annotation_text="Target 85%", annotation_font=dict(color="#ffaa00", size=10))
    fig.add_hline(y=95, line_dash="dot", line_color="rgba(0,255,136,0.5)",
                  annotation_text="Excellent 95%", annotation_font=dict(color="#00ff88", size=10))
    layout = base_layout("Quality Score — 24h Trend", height=295)
    layout["yaxis"]["range"] = [60, 100]
    fig.update_layout(**layout)
    return fig

def defect_rate_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["time"], y=df["defect_rate"], mode="lines", name="Defect %",
                             line=dict(color="#ff3355", width=2),
                             fill="tozeroy", fillcolor="rgba(255,51,85,0.05)"))
    fig.add_hline(y=2.0, line_dash="dot", line_color="rgba(255,170,0,0.5)",
                  annotation_text="Threshold 2%", annotation_font=dict(color="#ffaa00", size=10))
    layout = base_layout("Defect Rate — 24h Trend", height=295)
    layout["yaxis"]["range"] = [0, 6]
    fig.update_layout(**layout)
    return fig

def throughput_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["time"][::12], y=df["throughput"][::12],
                         name="Units/hr", marker_color="#a855f7", marker_line_width=0, opacity=0.85))
    layout = base_layout("Throughput — Units Per Hour", height=295)
    fig.update_layout(**layout)
    return fig

def sensor_multi_chart(df):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                        subplot_titles=("Temperature (°C)", "Pressure (hPa)"))
    fig.add_trace(go.Scatter(x=df["time"], y=df["temperature"],
                             line=dict(color="#ffaa00", width=1.5), name="Temp"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["time"], y=df["pressure"],
                             line=dict(color="#a855f7", width=1.5), name="Pressure"), row=2, col=1)
    fig.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                      font=dict(family=FONT_FAM, color=TEXT_CLR),
                      height=340, margin=dict(l=44, r=20, t=48, b=40), showlegend=False)
    fig.update_xaxes(gridcolor=GRID_CLR, linecolor=GRID_CLR)
    fig.update_yaxes(gridcolor=GRID_CLR, linecolor=GRID_CLR)
    for ann in fig["layout"]["annotations"]:
        ann["font"] = {"color": "#8899b3", "size": 11, "family": FONT_FAM}
    return fig

def vibration_chart(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["time"], y=df["vibration"], mode="lines", name="Vibration mm/s",
                             line=dict(color="#00ff88", width=1.5),
                             fill="tozeroy", fillcolor="rgba(0,255,136,0.05)"))
    fig.add_hline(y=4.5, line_dash="dash", line_color="rgba(255,51,85,0.5)",
                  annotation_text="Critical 4.5mm/s", annotation_font=dict(color="#ff3355", size=10))
    layout = base_layout("Vibration — mm/s", height=260)
    layout["yaxis"]["range"] = [0, 7]
    fig.update_layout(**layout)
    return fig

def defect_pareto_chart(df):
    df_s = df.sort_values("count", ascending=False)
    cumulative = df_s["count"].cumsum() / df_s["count"].sum() * 100
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df_s["category"], y=df_s["count"],
                         marker_color=["#ff3355","#ff5577","#ff7799","#ffaa00","#ffbb33","#a855f7"],
                         name="Count", marker_line_width=0), secondary_y=False)
    fig.add_trace(go.Scatter(x=df_s["category"], y=cumulative,
                             mode="lines+markers", name="Cumulative %",
                             line=dict(color="#00d4ff", width=2),
                             marker=dict(size=6, color="#00d4ff")), secondary_y=True)
    fig.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                      font=dict(family=FONT_FAM, color=TEXT_CLR),
                      height=340, margin=dict(l=44, r=44, t=48, b=60),
                      title=dict(text="Defect Pareto Analysis", font=dict(size=14, color="#e8edf5")),
                      legend=dict(bgcolor="rgba(0,0,0,0)"))
    fig.update_xaxes(gridcolor=GRID_CLR, tickangle=-30, tickfont=dict(size=10))
    fig.update_yaxes(gridcolor=GRID_CLR, title_text="Count", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative %", secondary_y=True, gridcolor="rgba(0,0,0,0)")
    return fig

def machine_heatmap(df_m):
    zones   = df_m["zone"].unique().tolist()
    metrics = ["quality_score", "oee", "uptime"]
    labels  = ["Quality %", "OEE %", "Uptime %"]
    z_vals, y_labels = [], []
    for z in zones:
        sub = df_m[df_m["zone"] == z]
        z_vals.append([sub[m].mean() for m in metrics])
        y_labels.append(z.split("–")[-1].strip())
    fig = go.Figure(go.Heatmap(
        z=z_vals, x=labels, y=y_labels,
        colorscale=[[0,"#ff3355"],[0.5,"#ffaa00"],[1,"#00ff88"]],
        zmin=60, zmax=100,
        text=[[f"{v:.1f}%" for v in row] for row in z_vals],
        texttemplate="%{text}",
        textfont=dict(size=13, color="white", family="Share Tech Mono"),
        hovertemplate="%{y}<br>%{x}: %{z:.1f}%<extra></extra>",
    ))
    fig.update_layout(paper_bgcolor=PAPER_BG, plot_bgcolor=PLOT_BG,
                      font=dict(family=FONT_FAM, color=TEXT_CLR),
                      height=270, margin=dict(l=110, r=20, t=48, b=40),
                      title=dict(text="Zone Performance Heatmap", font=dict(size=14, color="#e8edf5")),
                      xaxis=dict(side="top"))
    return fig

def scatter_quality_oee(df_m):
    status_colors = {"OPERATIONAL":"#00ff88","WARNING":"#ffaa00","CRITICAL":"#ff3355","IDLE":"#8899b3"}
    fig = go.Figure()
    for status, color in status_colors.items():
        sub = df_m[df_m["status"] == status]
        if len(sub):
            fig.add_trace(go.Scatter(
                x=sub["oee"], y=sub["quality_score"],
                mode="markers+text",
                marker=dict(size=13, color=color, line=dict(width=1.5, color="#0a0d12"), opacity=0.9),
                text=sub["machine"], textposition="top center",
                textfont=dict(size=9, color=color, family="Share Tech Mono"),
                name=status,
                hovertemplate="<b>%{text}</b><br>OEE: %{x:.1f}%<br>Quality: %{y:.1f}%<extra></extra>",
            ))
    layout = base_layout("Quality Score vs OEE", height=350)
    layout["xaxis"]["title"] = "OEE (%)"
    layout["yaxis"]["title"] = "Quality Score (%)"
    fig.update_layout(**layout)
    return fig

def shift_comparison_chart(df_s):
    fig = go.Figure()
    for shift_type, color in [("Day","#00d4ff"),("Night","#a855f7")]:
        sub = df_s[df_s["type"]==shift_type]
        fig.add_trace(go.Bar(
            x=sub["shift"].str.replace("Day–","").str.replace("Night–",""),
            y=sub["quality"], name=f"{shift_type} Shift",
            marker_color=color, marker_line_width=0, opacity=0.85,
        ))
    fig.add_hline(y=96, line_dash="dot", line_color="rgba(255,170,0,0.5)",
                  annotation_text="Target 96%", annotation_font=dict(color="#ffaa00", size=10))
    layout = base_layout("Shift Quality Comparison (%)", height=320)
    layout["yaxis"]["range"] = [88, 100]
    layout["barmode"] = "group"
    fig.update_layout(**layout)
    return fig

def cost_impact_chart(df):
    fig = go.Figure(go.Pie(
        labels=df["category"], values=df["cost_impact"], hole=0.62,
        marker=dict(colors=["#ff3355","#ff5577","#ff8899","#ffaa00","#ffbb33","#a855f7"],
                    line=dict(color=PLOT_BG, width=3)),
        textfont=dict(size=11, family=FONT_FAM, color="white"),
        hovertemplate="%{label}<br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig.add_annotation(text="Cost<br>Impact", x=0.5, y=0.5, showarrow=False,
                       font=dict(size=12, color="#8899b3", family=FONT_FAM))
    fig.update_layout(paper_bgcolor=PAPER_BG,
                      height=295, margin=dict(l=20, r=20, t=48, b=20),
                      title=dict(text="Defect Cost Distribution", font=dict(size=14, color="#e8edf5")),
                      legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)))
    return fig

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def kpi_card(label, value, unit, delta_txt, delta_up, color, icon, bar_pct=None):
    arrow    = "▲" if delta_up else "▼"
    d_class  = "delta-up" if delta_up else "delta-down"
    bar_html = ""
    if bar_pct is not None:
        bar_html = f"""
        <div class="kpi-bar">
          <div class="kpi-bar-fill" style="width:{bar_pct}%;background:{color};"></div>
        </div>"""
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-top">
        <div class="kpi-label">{label}</div>
        <div class="kpi-icon">{icon}</div>
      </div>
      <div class="kpi-value" style="color:{color};">{value}<span class="kpi-unit">{unit}</span></div>
      <div class="kpi-delta {d_class}">{arrow} {delta_txt}</div>
      {bar_html}
    </div>
    """, unsafe_allow_html=True)

def severity_badge(s):
    cls = {"CRITICAL":"badge-red","WARNING":"badge-amber","INFO":"badge-cyan"}.get(s,"badge-cyan")
    return f'<span class="badge {cls}">{s}</span>'

def status_badge(s):
    cls = {"OPERATIONAL":"badge-green","WARNING":"badge-amber","CRITICAL":"badge-red","IDLE":"badge-cyan"}.get(s,"badge-cyan")
    return f'<span class="badge {cls}">{s}</span>'

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-container">
      <div class="logo-icon">🏭</div>
      <div>
        <div class="logo-text-main">Industrial QM</div>
        <div class="logo-text-sub">Platform v2.4</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)
    page = st.radio("", [
        "📊  Dashboard",
        "🏭  Machine Monitor",
        "📈  Analytics",
        "🚨  Alerts & Events",
        "🔮  Forecasting",
        "⚙️  Settings",
    ], label_visibility="collapsed", key="page_radio")

    st.markdown("---")
    st.markdown('<div class="nav-label">Live Status</div>', unsafe_allow_html=True)
    now_str  = datetime.now().strftime("%H:%M:%S")
    date_str = datetime.now().strftime("%d %b %Y")
    st.markdown(f"""
    <div style="font-family:var(--font-mono);font-size:11px;color:#4a5a72;margin-bottom:6px;">{date_str}</div>
    <div class="timestamp">⏱ {now_str}</div>
    <div style="margin-top:10px;font-size:12px;color:#8899b3;">
      <span class="live-dot"></span> Live feed active
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="nav-label">Auto-Refresh</div>', unsafe_allow_html=True)

    # Store toggle state in session so page navigation doesn't reset it
    auto_refresh = st.toggle("Enable live updates", value=st.session_state.auto_refresh, key="ar_toggle")
    st.session_state.auto_refresh = auto_refresh

    refresh_interval = st.select_slider("Interval", options=[5, 10, 15, 30, 60],
                                        value=st.session_state.refresh_interval, key="ar_interval")
    st.session_state.refresh_interval = refresh_interval

    if auto_refresh:
        elapsed = time.time() - st.session_state.last_refresh
        remaining = max(0, refresh_interval - elapsed)
        st.markdown(f"""
        <div style="font-size:11px;color:#00ff88;font-family:var(--font-mono);">
          ● Next refresh in {int(remaining)}s
        </div>
        """, unsafe_allow_html=True)
        # Sleep remaining time then rerun — works on ALL pages
        if elapsed >= refresh_interval:
            st.session_state.last_refresh = time.time()
            time.sleep(0.1)
            st.rerun()
        else:
            time.sleep(1)
            st.rerun()

    st.markdown("---")
    st.markdown('<div class="nav-label">Quick Filters</div>', unsafe_allow_html=True)
    selected_zone = st.multiselect(
        "Zone", ["Zone A – Assembly","Zone B – Fabrication","Zone C – Finishing","Zone D – Packaging"],
        default=["Zone A – Assembly","Zone B – Fabrication","Zone C – Finishing","Zone D – Packaging"],
        label_visibility="collapsed"
    )
    time_window = st.select_slider("Time window",
                                   options=["1h","4h","8h","12h","24h"], value="24h")

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
hours_map = {"1h":1,"4h":4,"8h":8,"12h":12,"24h":24}
df   = generate_time_series(hours=hours_map[time_window])
df_m = generate_machine_data()
df_a = generate_alerts()
df_d = generate_defect_breakdown()
df_s = generate_shift_data()

if selected_zone:
    df_m = df_m[df_m["zone"].isin(selected_zone)]

current_quality    = float(df["quality"].iloc[-1])
current_defect     = float(df["defect_rate"].iloc[-1])
current_throughput = float(df["throughput"].iloc[-1])
current_vibration  = float(df["vibration"].iloc[-1])
avg_oee            = float(df_m["oee"].mean()) if len(df_m) else 0
active_alerts      = len(df_a[df_a["severity"]=="CRITICAL"])
machines_total     = len(df_m)
machines_ok        = len(df_m[df_m["status"]=="OPERATIONAL"])

# ─────────────────────────────────────────────
# PAGE: DASHBOARD
# ─────────────────────────────────────────────
if page == "📊  Dashboard":
    st.markdown(f"""
    <div class="hero-banner">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:6px;">
        <span class="live-dot"></span>
        <span style="font-family:var(--font-mono);font-size:11px;color:#8899b3;letter-spacing:2px;">LIVE OPERATIONS</span>
      </div>
      <div class="hero-title">Industrial Quality Monitoring Platform</div>
      <div class="hero-sub">{datetime.now().strftime('%A, %d %B %Y · %H:%M:%S')} · {machines_ok}/{machines_total} machines online</div>
    </div>
    """, unsafe_allow_html=True)

    # Critical alerts
    for _, row in df_a[df_a["severity"]=="CRITICAL"].iterrows():
        mins_ago = int((datetime.now()-row["time"]).total_seconds()//60)
        st.markdown(f"""
        <div class="alert-critical">
          🚨 <strong>{row['machine']}</strong> — {row['message']}
          <span style="float:right;font-size:11px;color:rgba(255,51,85,0.6);">{mins_ago}m ago</span>
        </div>
        """, unsafe_allow_html=True)

    # ── KPI ROW 1: 3 cards
    st.markdown('<div class="section-title">Key Performance Indicators</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Quality Score", f"{current_quality:.1f}", "%",
                 "+1.3% vs yesterday", True, "#00d4ff", "🎯", bar_pct=current_quality)
    with c2:
        is_bad = current_defect > 2
        kpi_card("Defect Rate", f"{current_defect:.2f}", "%",
                 "-0.18% this shift", True, "#ff3355" if is_bad else "#00ff88", "⚠️",
                 bar_pct=min(current_defect*20, 100))
    with c3:
        kpi_card("Throughput", f"{current_throughput:.0f}", " u/h",
                 "on track for target", True, "#a855f7", "⚡", bar_pct=current_throughput/10)

    # ── KPI ROW 2: 3 cards
    c4, c5, c6 = st.columns(3)
    with c4:
        oee_ok = avg_oee >= 85
        kpi_card("OEE", f"{avg_oee:.1f}", "%",
                 "+2.1% vs last week", True, "#00ff88" if oee_ok else "#ffaa00", "🔧", bar_pct=avg_oee)
    with c5:
        kpi_card("Active Alerts", f"{active_alerts}", "",
                 "2 acknowledged", False if active_alerts > 0 else True,
                 "#ff3355" if active_alerts > 0 else "#00ff88", "🚨",
                 bar_pct=min(active_alerts*20, 100))
    with c6:
        vib_ok = current_vibration <= 3.5
        kpi_card("Vibration", f"{current_vibration:.2f}", " mm/s",
                 "within tolerance" if vib_ok else "above threshold",
                 vib_ok, "#00ff88" if vib_ok else "#ffaa00", "📡",
                 bar_pct=min(current_vibration/6*100, 100))

    # Gauges + trend
    st.markdown('<div class="section-title">Quality & OEE Gauges</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns([1, 1, 2])
    with g1:
        st.plotly_chart(quality_gauge(current_quality), use_container_width=True)
    with g2:
        st.plotly_chart(oee_gauge(avg_oee), use_container_width=True)
    with g3:
        st.plotly_chart(quality_trend_chart(df), use_container_width=True)

    # Charts
    st.markdown('<div class="section-title">Operational Metrics</div>', unsafe_allow_html=True)
    ch1, ch2 = st.columns(2)
    with ch1:
        st.plotly_chart(defect_rate_chart(df), use_container_width=True)
    with ch2:
        st.plotly_chart(throughput_chart(df), use_container_width=True)

    # Recent events table
    st.markdown('<div class="section-title">Recent Events</div>', unsafe_allow_html=True)
    rows_html = ""
    for _, row in df_a.head(6).iterrows():
        mins_ago = int((datetime.now()-row["time"]).total_seconds()//60)
        rows_html += f"""
        <tr>
          <td style="font-family:var(--font-mono);font-size:11px;color:#4a5a72;">{mins_ago}m ago</td>
          <td>{severity_badge(row['severity'])}</td>
          <td style="font-family:var(--font-mono);color:#00d4ff;">{row['machine']}</td>
          <td>{row['message']}</td>
        </tr>"""
    st.markdown(f"""
    <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;overflow:hidden;">
      <table class="event-table">
        <thead><tr><th>Time</th><th>Severity</th><th>Machine</th><th>Event</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: MACHINE MONITOR
# ─────────────────────────────────────────────
elif page == "🏭  Machine Monitor":
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-title">Machine Monitor</div>
      <div class="hero-sub">Unit-level status · sensor readings · health indicators</div>
    </div>
    """, unsafe_allow_html=True)

    op   = len(df_m[df_m["status"]=="OPERATIONAL"])
    warn = len(df_m[df_m["status"]=="WARNING"])
    crit = len(df_m[df_m["status"]=="CRITICAL"])
    idle = len(df_m[df_m["status"]=="IDLE"])
    st.markdown(f"""
    <div style="display:flex;gap:12px;margin-bottom:18px;flex-wrap:wrap;">
      <span class="badge badge-green">✔ {op} Operational</span>
      <span class="badge badge-amber">⚠ {warn} Warning</span>
      <span class="badge badge-red">✖ {crit} Critical</span>
      <span class="badge badge-cyan">◌ {idle} Idle</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Unit Status Grid</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (_, row) in enumerate(df_m.iterrows()):
        sc = {"OPERATIONAL":"#00ff88","WARNING":"#ffaa00","CRITICAL":"#ff3355","IDLE":"#8899b3"}.get(row["status"],"#8899b3")
        with cols[i % 4]:
            st.markdown(f"""
            <div class="machine-card" style="border-color:rgba({','.join(str(int(sc.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.35);
                 box-shadow:0 0 18px rgba({','.join(str(int(sc.lstrip('#')[i:i+2],16)) for i in (0,2,4))},0.08);">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                <span style="font-family:var(--font-mono);font-size:14px;font-weight:700;color:{sc};">{row['machine']}</span>
                {status_badge(row['status'])}
              </div>
              <div style="font-size:10px;color:#4a5a72;margin-bottom:10px;font-family:var(--font-mono);">{row['zone']}</div>
              <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
                <div><div style="font-size:9px;color:#4a5a72;margin-bottom:2px;">QUALITY</div>
                     <div style="font-family:var(--font-mono);font-size:16px;color:#00d4ff;">{row['quality_score']:.1f}%</div></div>
                <div><div style="font-size:9px;color:#4a5a72;margin-bottom:2px;">OEE</div>
                     <div style="font-family:var(--font-mono);font-size:16px;color:#a855f7;">{row['oee']:.1f}%</div></div>
                <div><div style="font-size:9px;color:#4a5a72;margin-bottom:2px;">TEMP</div>
                     <div style="font-family:var(--font-mono);font-size:13px;color:#ffaa00;">{row['temperature']:.0f}°C</div></div>
                <div><div style="font-size:9px;color:#4a5a72;margin-bottom:2px;">VIBRATION</div>
                     <div style="font-family:var(--font-mono);font-size:13px;color:{'#ff3355' if row['vibration']>4.0 else '#00ff88'};">{row['vibration']:.2f}</div></div>
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Zone & Machine Performance</div>', unsafe_allow_html=True)
    h1, h2 = st.columns([1.2, 1])
    with h1:
        st.plotly_chart(machine_heatmap(df_m), use_container_width=True)
    with h2:
        st.plotly_chart(scatter_quality_oee(df_m), use_container_width=True)

    st.markdown('<div class="section-title">Detailed Machine Table</div>', unsafe_allow_html=True)
    rows_html = ""
    for _, row in df_m.iterrows():
        v_color = "#ff3355" if row["vibration"] > 4.0 else "#e8edf5"
        t_color = "#ff3355" if row["temperature"] > 88 else "#ffaa00" if row["temperature"] > 80 else "#e8edf5"
        rows_html += f"""
        <tr>
          <td style="font-family:var(--font-mono);color:#00d4ff;">{row['machine']}</td>
          <td style="color:#4a5a72;font-size:11px;">{row['zone']}</td>
          <td>{status_badge(row['status'])}</td>
          <td style="font-family:var(--font-mono);">{row['quality_score']:.1f}%</td>
          <td style="font-family:var(--font-mono);">{row['oee']:.1f}%</td>
          <td style="font-family:var(--font-mono);color:{t_color};">{row['temperature']:.0f}°C</td>
          <td style="font-family:var(--font-mono);color:{v_color};">{row['vibration']:.2f} mm/s</td>
          <td style="font-family:var(--font-mono);">{row['uptime']:.1f}%</td>
        </tr>"""
    st.markdown(f"""
    <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;overflow:hidden;">
      <table class="event-table">
        <thead><tr><th>Unit</th><th>Zone</th><th>Status</th><th>Quality</th><th>OEE</th><th>Temp</th><th>Vibration</th><th>Uptime</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: ANALYTICS
# ─────────────────────────────────────────────
elif page == "📈  Analytics":
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-title">Quality Analytics</div>
      <div class="hero-sub">Sensor deep-dive · Pareto · shift benchmarking · defect intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Sensor Time-Series</div>', unsafe_allow_html=True)
    s1, s2 = st.columns(2)
    with s1:
        st.plotly_chart(sensor_multi_chart(df), use_container_width=True)
    with s2:
        st.plotly_chart(vibration_chart(df), use_container_width=True)

    st.markdown('<div class="section-title">Defect Intelligence</div>', unsafe_allow_html=True)
    d1, d2 = st.columns([2, 1])
    with d1:
        st.plotly_chart(defect_pareto_chart(df_d), use_container_width=True)
    with d2:
        st.plotly_chart(cost_impact_chart(df_d), use_container_width=True)

    total_count = df_d["count"].sum()
    rows_html = ""
    for _, row in df_d.sort_values("count", ascending=False).iterrows():
        pct = row["count"]/total_count*100
        bar = "█"*int(pct/5) + "░"*(20-int(pct/5))
        rows_html += f"""
        <tr>
          <td>{row['category']}</td>
          <td style="font-family:var(--font-mono);">{row['count']}</td>
          <td style="font-family:var(--font-mono);font-size:10px;color:#4a5a72;">{bar}</td>
          <td style="font-family:var(--font-mono);">{pct:.1f}%</td>
          <td style="font-family:var(--font-mono);color:#ffaa00;">₹{row['cost_impact']:,}</td>
        </tr>"""
    st.markdown(f"""
    <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;overflow:hidden;margin-top:8px;">
      <table class="event-table">
        <thead><tr><th>Defect Category</th><th>Count</th><th>Proportion</th><th>% of Total</th><th>Cost Impact</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Shift Performance Benchmarking</div>', unsafe_allow_html=True)
    st.plotly_chart(shift_comparison_chart(df_s), use_container_width=True)

    rows_html = ""
    for _, row in df_s.iterrows():
        q_color = "#00ff88" if row["quality"]>=97 else "#ffaa00" if row["quality"]>=95 else "#ff3355"
        rows_html += f"""
        <tr>
          <td>{row['shift']}</td>
          <td><span class="badge badge-cyan">{row['type'].upper()}</span></td>
          <td style="font-family:var(--font-mono);">{row['units']}</td>
          <td style="font-family:var(--font-mono);color:#ff3355;">{row['defects']}</td>
          <td style="font-family:var(--font-mono);color:{q_color};">{row['quality']:.1f}%</td>
          <td style="font-family:var(--font-mono);">{row['defects']/row['units']*100:.2f}%</td>
        </tr>"""
    st.markdown(f"""
    <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;overflow:hidden;">
      <table class="event-table">
        <thead><tr><th>Shift</th><th>Type</th><th>Units</th><th>Defects</th><th>Quality</th><th>Defect Rate</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: ALERTS & EVENTS
# ─────────────────────────────────────────────
elif page == "🚨  Alerts & Events":
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-title">Alerts & Events</div>
      <div class="hero-sub">Event log · anomaly detection · escalation tracking</div>
    </div>
    """, unsafe_allow_html=True)

    col_f1, _ = st.columns([1, 3])
    with col_f1:
        sev_filter = st.multiselect("Severity", ["CRITICAL","WARNING","INFO"],
                                    default=["CRITICAL","WARNING","INFO"])

    df_filtered = df_a[df_a["severity"].isin(sev_filter)] if sev_filter else df_a

    c1, c2, c3 = st.columns(3)
    with c1:
        kpi_card("Critical", str(len(df_a[df_a["severity"]=="CRITICAL"])), "",
                 "last 24h", False, "#ff3355", "🔴")
    with c2:
        kpi_card("Warnings", str(len(df_a[df_a["severity"]=="WARNING"])), "",
                 "last 24h", False, "#ffaa00", "🟡")
    with c3:
        kpi_card("Info", str(len(df_a[df_a["severity"]=="INFO"])), "",
                 "last 24h", True, "#00d4ff", "🔵")

    st.markdown('<div class="section-title">Event Log</div>', unsafe_allow_html=True)
    for _, row in df_filtered.iterrows():
        mins_ago = int((datetime.now()-row["time"]).total_seconds()//60)
        if row["severity"]=="CRITICAL":
            cls, icon = "alert-critical","🚨"
        elif row["severity"]=="WARNING":
            cls, icon = "alert-warning","⚠️"
        else:
            cls, icon = "alert-ok","ℹ️"
        st.markdown(f"""
        <div class="{cls}">
          {icon} <strong>{row['machine']}</strong> — {row['message']}
          <span style="float:right;font-size:11px;opacity:0.6;">{severity_badge(row['severity'])} &nbsp; {mins_ago}m ago</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Alert Timeline</div>', unsafe_allow_html=True)
    sev_c = {"CRITICAL":"#ff3355","WARNING":"#ffaa00","INFO":"#00d4ff"}
    fig_t = go.Figure()
    for sev, color in sev_c.items():
        sub = df_a[df_a["severity"]==sev]
        fig_t.add_trace(go.Scatter(
            x=sub["time"], y=[sev]*len(sub), mode="markers", name=sev,
            marker=dict(size=16, color=color, symbol="diamond", line=dict(width=1.5, color="#0a0d12")),
            text=sub["message"], hovertemplate="<b>%{text}</b><extra></extra>",
        ))
    layout_t = base_layout("", height=200)
    layout_t["yaxis"]["gridcolor"] = "rgba(0,0,0,0)"
    layout_t["margin"] = dict(l=80, r=20, t=20, b=40)
    fig_t.update_layout(**layout_t)
    st.plotly_chart(fig_t, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE: FORECASTING
# ─────────────────────────────────────────────
elif page == "🔮  Forecasting":
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-title">Predictive Forecasting</div>
      <div class="hero-sub">Quality trajectory · defect prediction · maintenance windows</div>
    </div>
    """, unsafe_allow_html=True)

    rng = np.random.default_rng(int(time.time() // 5))
    last_val = float(df["quality"].iloc[-1])
    forecast_hours = 8
    future_times = [datetime.now() + timedelta(minutes=i*15) for i in range(forecast_hours*4)]
    trend = rng.normal(0, 0.15, len(future_times))
    forecast_vals = np.clip(last_val + np.cumsum(trend) + 2*np.sin(np.linspace(0, 2*np.pi, len(future_times))), 70, 99)
    upper = np.clip(forecast_vals + np.linspace(0.5, 3.5, len(future_times)), 70, 100)
    lower = np.clip(forecast_vals - np.linspace(0.5, 3.5, len(future_times)), 65, 99)

    fig_f = go.Figure()
    fig_f.add_trace(go.Scatter(x=df["time"].iloc[-48:], y=df["quality"].iloc[-48:],
                                mode="lines", name="Actual", line=dict(color="#00d4ff", width=2)))
    fig_f.add_trace(go.Scatter(
        x=future_times + future_times[::-1],
        y=list(upper) + list(lower[::-1]),
        fill="toself", fillcolor="rgba(168,85,247,0.12)", line_color="rgba(0,0,0,0)",
        name="Confidence Band",
    ))
    fig_f.add_trace(go.Scatter(x=future_times, y=forecast_vals, mode="lines", name="Forecast",
                                line=dict(color="#a855f7", width=2, dash="dot")))
    fig_f.add_vline(x=datetime.now(), line_dash="dash", line_color="rgba(255,170,0,0.4)",
                     annotation_text="Now", annotation_font=dict(color="#ffaa00", size=11))
    layout_f = base_layout("Quality Score Forecast — Next 8 Hours", height=380)
    layout_f["yaxis"]["range"] = [65, 100]
    fig_f.update_layout(**layout_f)
    st.plotly_chart(fig_f, use_container_width=True)

    st.markdown('<div class="section-title">Predictive Maintenance Windows</div>', unsafe_allow_html=True)
    maint_data = [
        {"machine":"UNIT-005","component":"Bearing Assembly","risk":"HIGH",   "hours_remaining":12,"confidence":91},
        {"machine":"UNIT-003","component":"Cooling System",  "risk":"MEDIUM", "hours_remaining":38,"confidence":78},
        {"machine":"UNIT-011","component":"Pressure Valve",  "risk":"MEDIUM", "hours_remaining":52,"confidence":71},
        {"machine":"UNIT-008","component":"Drive Belt",      "risk":"LOW",    "hours_remaining":96,"confidence":64},
        {"machine":"UNIT-001","component":"Sensor Array",    "risk":"LOW",    "hours_remaining":144,"confidence":58},
    ]
    risk_cls = {"HIGH":"badge-red","MEDIUM":"badge-amber","LOW":"badge-cyan"}
    rows_html = ""
    for r in maint_data:
        rows_html += f"""
        <tr>
          <td style="font-family:var(--font-mono);color:#00d4ff;">{r['machine']}</td>
          <td>{r['component']}</td>
          <td><span class="badge {risk_cls[r['risk']]}">{r['risk']}</span></td>
          <td style="font-family:var(--font-mono);">{r['hours_remaining']}h</td>
          <td style="font-family:var(--font-mono);color:#a855f7;">{r['confidence']}%</td>
        </tr>"""
    st.markdown(f"""
    <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;overflow:hidden;">
      <table class="event-table">
        <thead><tr><th>Unit</th><th>Component</th><th>Risk Level</th><th>Est. Remaining</th><th>Model Confidence</th></tr></thead>
        <tbody>{rows_html}</tbody>
      </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Defect Rate Forecast</div>', unsafe_allow_html=True)
    d_last = float(df["defect_rate"].iloc[-1])
    d_trend = rng.normal(-0.01, 0.05, len(future_times))
    d_forecast = np.clip(d_last + np.cumsum(d_trend), 0.2, 5.0)
    d_upper = np.clip(d_forecast + np.linspace(0.1, 0.8, len(future_times)), 0.1, 6.0)
    d_lower = np.clip(d_forecast - np.linspace(0.1, 0.8, len(future_times)), 0.0, 5.0)
    fig_d = go.Figure()
    fig_d.add_trace(go.Scatter(x=df["time"].iloc[-48:], y=df["defect_rate"].iloc[-48:],
                                mode="lines", name="Actual", line=dict(color="#ff3355", width=2)))
    fig_d.add_trace(go.Scatter(
        x=future_times+future_times[::-1], y=list(d_upper)+list(d_lower[::-1]),
        fill="toself", fillcolor="rgba(255,51,85,0.08)", line_color="rgba(0,0,0,0)", name="Confidence"))
    fig_d.add_trace(go.Scatter(x=future_times, y=d_forecast, mode="lines", name="Forecast",
                                line=dict(color="#ffaa00", width=2, dash="dot")))
    fig_d.add_hline(y=2.0, line_dash="dash", line_color="rgba(255,51,85,0.4)",
                     annotation_text="Threshold", annotation_font=dict(color="#ff3355", size=10))
    fig_d.add_vline(x=datetime.now(), line_dash="dash", line_color="rgba(255,170,0,0.4)")
    layout_d = base_layout("Defect Rate Forecast (%)", height=300)
    layout_d["yaxis"]["range"] = [0, 5]
    fig_d.update_layout(**layout_d)
    st.plotly_chart(fig_d, use_container_width=True)


# ─────────────────────────────────────────────
# PAGE: SETTINGS
# ─────────────────────────────────────────────
elif page == "⚙️  Settings":
    st.markdown("""
    <div class="hero-banner">
      <div class="hero-title">Platform Settings</div>
      <div class="hero-sub">Alert thresholds · notification rules · data configuration</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Alert Thresholds</div>', unsafe_allow_html=True)
        st.slider("Quality Score — Warning threshold (%)", 70, 95, 85)
        st.slider("Quality Score — Critical threshold (%)", 60, 85, 75)
        st.slider("Defect Rate — Warning threshold (%)", 1.0, 5.0, 2.0, step=0.1)
        st.slider("Vibration — Warning threshold (mm/s)", 2.0, 6.0, 3.5, step=0.1)
        st.slider("Temperature — Critical threshold (°C)", 70, 110, 90)
        st.markdown('<div class="section-title">Data Configuration</div>', unsafe_allow_html=True)
        st.selectbox("Data retention period", ["7 days","14 days","30 days","90 days","1 year"])
        st.selectbox("Sampling rate", ["5 seconds","15 seconds","30 seconds","1 minute","5 minutes"])
        st.selectbox("Timezone", ["IST (UTC+5:30)","UTC","EST (UTC-5)","PST (UTC-8)"])

    with col2:
        st.markdown('<div class="section-title">Notification Rules</div>', unsafe_allow_html=True)
        st.toggle("Email alerts — Critical", value=True)
        st.toggle("Email alerts — Warning",  value=True)
        st.toggle("SMS alerts — Critical only", value=False)
        st.toggle("Dashboard push notifications", value=True)
        st.toggle("Slack integration", value=False)
        st.text_input("Alert email recipients", "ops-team@company.com")
        st.text_input("Slack webhook URL", placeholder="#quality-ops channel")
        st.markdown('<div class="section-title">System Info</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:10px;padding:18px;font-family:var(--font-mono);font-size:12px;line-height:2.1;">
          <div><span style="color:#4a5a72;">Platform Version &nbsp;</span><span style="color:#00d4ff;">v2.4.1</span></div>
          <div><span style="color:#4a5a72;">Last Updated &nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:#e8edf5;">{datetime.now().strftime('%d %b %Y')}</span></div>
          <div><span style="color:#4a5a72;">Machines Connected </span><span style="color:#00ff88;">{machines_total}</span></div>
          <div><span style="color:#4a5a72;">Data Points / 24h &nbsp;</span><span style="color:#a855f7;">288,000</span></div>
          <div><span style="color:#4a5a72;">Model Engine &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:#ffaa00;">IQ-Predict 3.1</span></div>
          <div><span style="color:#4a5a72;">Uptime (30d) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span style="color:#00ff88;">99.97%</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    sc1, sc2, _ = st.columns([1, 1, 4])
    with sc1:
        if st.button("💾  Save Settings", use_container_width=True):
            st.success("Settings saved.")
    with sc2:
        if st.button("↺  Reset Defaults", use_container_width=True):
            st.info("Settings reset to defaults.")