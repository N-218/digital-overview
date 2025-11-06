import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Digital Oversight Dashboard",
    layout="wide",
    page_icon="💼",
    initial_sidebar_state="expanded"
)

# =========================
# BLUE & WHITE PREMIUM THEME
# =========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
        font-family: 'Inter', 'Segoe UI', sans-serif;
        color: #1e293b;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 95% !important;
    }
    .dashboard-header {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);
        color: white;
        margin-bottom: 35px;
    }
    .dashboard-header h1 {
        margin: 0;
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #fff !important;
    }
    .dashboard-header p {
        margin-top: 10px;
        font-size: 16px;
        color: rgba(255,255,255,0.9);
    }
    .content-card {
        background: #ffffff;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 8px 20px rgba(0,64,128,0.08);
        margin-bottom: 25px;
        transition: all 0.3s ease-in-out;
    }
    .content-card:hover {
        box-shadow: 0 10px 30px rgba(0,64,128,0.12);
        transform: translateY(-2px);
    }
    h2, h3, h4 {
        color: #0f3d91 !important;
        font-weight: 700;
        letter-spacing: -0.3px;
    }
    p, li {
        color: #334155;
        font-size: 15px;
        line-height: 1.5;
    }
    [data-testid="stMetricValue"] {
        color: #1e3a8a;
        font-size: 30px;
        font-weight: 700;
    }
    [data-testid="stMetricLabel"] {
        color: #64748b;
        font-weight: 600;
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f1f5ff 100%);
        border-right: 1px solid #e2e8f0;
    }
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] p {
        color: #0f3d91 !important;
        font-weight: 500;
    }
    .stButton > button {
        background: linear-gradient(90deg, #1d4ed8 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6rem 1.2rem;
        transition: all 0.2s ease-in-out;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #1e40af 0%, #1d4ed8 100%);
        transform: translateY(-1px);
        box-shadow: 0 4px 10px rgba(29,78,216,0.25);
    }
    .streamlit-expanderHeader {
        background-color: #f1f5f9;
        color: #0f3d91 !important;
        border-radius: 8px;
        font-weight: 600;
    }
    .footer {
        background: #f1f5f9;
        padding: 16px;
        border-radius: 10px;
        text-align: center;
        font-size: 13px;
        color: #64748b;
        margin-top: 30px;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div class='dashboard-header'>
    <h1>💼 Digital Oversight Dashboard</h1>
    <p>Production Forecast • Risk Monitoring • Strategic Roadmap</p>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR UPLOAD
# =========================
with st.sidebar:
    st.markdown("## 📂 Data Upload")
    uploaded_file = st.file_uploader("Upload Forecast CSV", type=["csv"])
    if uploaded_file is None:
        st.info("👆 Please upload your CSV file to begin")
        st.stop()
    df = pd.read_csv(uploaded_file)

# Mock preprocessing for demo
if "Risk_Level" not in df.columns:
    df["Year"] = range(2020, 2020 + len(df))
    df["Risk_Level"] = ["Low", "Medium", "High"] * (len(df)//3)
    df["Predicted_Gap"] = abs(df.index * 10 % 300)
    df["ProductionGap"] = abs(df.index * 8 % 280)
    df["Orders"] = 500 + df.index * 10
    df["Backlog"] = abs(df.index * 15 % 350)
    df["PlannedOutput"] = 400 + df.index * 8
    df["ActualOutput"] = 390 + df.index * 7

risk_map = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_map)

# =========================
# KPIs
# =========================
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("## 📊 Executive Summary")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Predicted Gap", f"{df['Predicted_Gap'].sum():,.0f}")
col2.metric("Avg Risk Score", f"{df['Risk_Score'].mean():.2f}/3")
col3.metric("Total Orders", f"{df['Orders'].sum():,.0f}")
col4.metric("Avg Backlog", f"{df['Backlog'].mean():,.0f}")
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# CHARTS
# =========================
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("## 📈 Forecast & Risk Overview")

colA, colB = st.columns(2)

primary_blue = "#2563eb"
secondary_blue = "#3b82f6"
teal = "#06b6d4"

with colA:
    st.markdown("### Production Gap Forecast")
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df["Year"], y=df["ProductionGap"], mode='lines+markers',
                              name="Historical Gap", line=dict(color=primary_blue, width=3)))
    fig1.add_trace(go.Scatter(x=df["Year"], y=df["Predicted_Gap"], mode='lines+markers',
                              name="Predicted Gap", line=dict(color=teal, width=3, dash='dot')))
    fig1.update_layout(height=400, template="plotly_white", hovermode='x unified',
                       legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
                       margin=dict(l=0, r=0, t=20, b=0),
                       plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.markdown("### Risk Levels by Year")
    fig2 = px.bar(df, x="Year", y="Risk_Score", color="Risk_Level",
                  color_discrete_map={"Low": "#3b82f6", "Medium": "#facc15", "High": "#ef4444"},
                  text="Risk_Level")
    fig2.update_traces(textposition='outside')
    fig2.update_layout(height=400, template="plotly_white",
                       legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
                       margin=dict(l=0, r=0, t=20, b=0),
                       plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ROADMAP SECTION
# =========================
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("## 🛣️ Strategic Roadmap")

roadmap_data = [
    {"Phase": "Q1 2025", "Goal": "Implement Predictive Analytics", "Status": "✅ Completed"},
    {"Phase": "Q2 2025", "Goal": "Enhance Risk Forecasting Models", "Status": "🟡 In Progress"},
    {"Phase": "Q3 2025", "Goal": "Integrate Supplier Data", "Status": "🔵 Planned"},
    {"Phase": "Q4 2025", "Goal": "Launch Global Oversight 2.0", "Status": "⚪ Upcoming"}
]
roadmap_df = pd.DataFrame(roadmap_data)

fig5 = px.timeline(
    roadmap_df,
    x_start=["2025-01-01", "2025-04-01", "2025-07-01", "2025-10-01"],
    x_end=["2025-03-31", "2025-06-30", "2025-09-30", "2025-12-31"],
    y="Phase",
    color="Status",
    text="Goal",
    color_discrete_map={"✅ Completed": "#22c55e", "🟡 In Progress": "#eab308",
                        "🔵 Planned": "#3b82f6", "⚪ Upcoming": "#94a3b8"}
)
fig5.update_layout(
    height=400,
    template="plotly_white",
    showlegend=True,
    xaxis_title="Timeline",
    yaxis_title="",
    margin=dict(l=0, r=0, t=20, b=0),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig5, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class='footer'>
    © 2025 Digital Oversight Dashboard • Designed for Executive Insights • Blue-White Professional Edition
</div>
""", unsafe_allow_html=True)
