import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# PAGE CONFIGURATION
# =========================
st.set_page_config(
    page_title="Boeing Digital Oversight Dashboard",
    layout="wide",
    page_icon="✈️"
)

# =========================
# BLUE–WHITE VISUAL THEME
# =========================
st.markdown("""
<style>
    /* ---- Base Layout ---- */
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

    /* ---- Boeing Watermark ---- */
    .stApp::before {
        content: "";
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/3/36/Boeing_full_logo.svg");
        background-size: 15%;
        background-repeat: no-repeat;
        background-position: top right;
        opacity: 0.06;
        position: fixed;
        top: 0; right: 0; bottom: 0; left: 0;
        z-index: 0;
    }

    /* ---- Dashboard Header ---- */
    .dashboard-header {
        background: linear-gradient(135deg, #1e40af 0%, #2563eb 100%);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        color: white;
        box-shadow: 0 8px 24px rgba(37, 99, 235, 0.25);
        margin-bottom: 40px;
    }
    .dashboard-header h1 {
        font-size: 40px;
        font-weight: 800;
        margin-bottom: 5px;
        color: white !important;
    }
    .dashboard-header p {
        font-size: 16px;
        color: rgba(255,255,255,0.9);
        margin: 0;
    }

    /* ---- Card Style ---- */
    .card {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        margin-bottom: 20px;
    }

    /* ---- Footer ---- */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR: DATA + FILTERS
# =========================
st.sidebar.title("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload Digital_Oversight_Forecast.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload your CSV file to continue.")
    st.stop()

# Map risk levels to numeric
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

st.sidebar.header("🔍 Filters")
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)
risk_levels = st.sidebar.multiselect(
    "Select Risk Levels",
    df["Risk_Level"].unique(),
    default=df["Risk_Level"].unique()
)

df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]

# =========================
# HEADER
# =========================
st.markdown("""
<div class="dashboard-header">
    <h1>✈️ Boeing Digital Oversight Dashboard</h1>
    <p>Forecast • Risk • Roadmap</p>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI SECTION
# =========================
st.markdown("### 🚩 Key Metrics")
with st.container():
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Predicted Gap", f"{df_filtered['Predicted_Gap'].sum():,.0f}")
    c2.metric("Max Risk Score", f"{df_filtered['Risk_Score'].max()}")
    c3.metric("Year with Highest Risk", f"{df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']}")
    c4.metric("Total Orders", f"{df_filtered['Orders'].sum():,}")

st.markdown("---")

# =========================
# FORECAST + RISK CHARTS
# =========================
st.markdown("### 📊 Forecast & Risk Overview")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        df_filtered,
        x="Year",
        y=["ProductionGap", "Predicted_Gap"],
        markers=True,
        labels={"value": "Gap", "variable": "Type"},
        title="Production Gap Forecast (2021–2028)",
        color_discrete_sequence=["#2563eb", "#1e3a8a"]
    )
    fig1.update_layout(title_x=0.5, template="plotly_white", height=350)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(
        df_filtered,
        x="Year",
        y="Risk_Score",
        color="Risk_Level",
        text="Risk_Score",
        title="Risk Levels by Year",
        color_discrete_map={"Low": "#22c55e", "Medium": "#facc15", "High": "#ef4444"}
    )
    fig2.update_layout(title_x=0.5, template="plotly_white", height=350)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# =========================
# ROADMAP SECTION
# =========================
st.markdown("### 🗺️ Implementation Roadmap (2025)")
phases = pd.DataFrame([
    dict(Phase='Planning & Vendor Setup', Start='2025-01-01', Finish='2025-02-28', Category='Planning'),
    dict(Phase='Telemetry Installation', Start='2025-03-01', Finish='2025-04-30', Category='Implementation'),
    dict(Phase='Supplier Integration', Start='2025-05-01', Finish='2025-06-30', Category='Integration'),
    dict(Phase='Pilot & Analytics', Start='2025-07-01', Finish='2025-12-31', Category='Analytics'),
    dict(Phase='Dashboard Deployment', Start='2025-07-01', Finish='2025-12-31', Category='Dashboard'),
    dict(Phase='Review & Scale Decision', Start='2025-12-31', Finish='2025-12-31', Category='Review')
])

phases["Start"] = pd.to_datetime(phases["Start"])
phases["Finish"] = pd.to_datetime(phases["Finish"])

colors = {
    'Planning': '#3b82f6',
    'Implementation': '#22c55e',
    'Integration': '#8b5cf6',
    'Analytics': '#facc15',
    'Dashboard': '#0ea5e9',
    'Review': '#ef4444'
}

fig3 = px.timeline(
    phases,
    x_start="Start",
    x_end="Finish",
    y="Phase",
    color="Category",
    color_discrete_map=colors,
)
fig3.update_yaxes(autorange="reversed")
fig3.update_layout(
    height=320, title_x=0.5, template="plotly_white",
    margin=dict(l=10, r=10, t=40, b=10)
)
st.plotly_chart(fig3, use_container_width=True)

# =========================
# RECOMMENDATIONS
# =========================
st.markdown("### 💡 Recommendations")
with st.expander("Click to view insights"):
    high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]["Year"].tolist()
    if high_gap_years:
        st.markdown(f"- ⚠️ High predicted gaps in {', '.join(map(str, high_gap_years))} — prioritize oversight.")
    else:
        st.markdown("- ✅ All predicted gaps within normal range.")

    st.markdown("""
    - 📡 Integrate digital telemetry for predictive monitoring.  
    - 🔔 Automate alerts for suppliers exceeding KPI thresholds.  
    - 📈 Focus on years with high Risk Score for proactive intervention.  
    - 🧭 Align roadmap execution with analytics insights for maximum ROI.  
    """)

# =========================
# FOOTER
# =========================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:13px;'>© 2025 Boeing | Digital Oversight Pilot | Streamlit Dashboard</p>", unsafe_allow_html=True)
