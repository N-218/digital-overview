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
# CUSTOM STYLE (Blue & White Theme)
# =========================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to bottom right, #f9fbfd, #ffffff);
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #0a3d62;
    font-weight: 600;
}
hr {
    border: 1px solid #dfe6e9;
}
[data-testid="stMetricValue"] {
    color: #1e3a8a !important;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 1rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR (Upload & Filters)
# =========================
st.sidebar.title("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload Digital_Oversight_Forecast.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload your CSV file to continue.")
    st.stop()

# Convert Risk Level to Numeric Score
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# Sidebar Filters
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
<div style='text-align:center;'>
<h1>✈️ Boeing Digital Oversight Dashboard</h1>
<p style='color:#34495e; font-size:16px;'>Forecast | Risk | Roadmap</p>
<hr style='width:50%; margin:auto;'>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI METRICS
# =========================
st.markdown("### 🚩 Key Insights")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Predicted Gap", f"{df_filtered['Predicted_Gap'].sum():,.0f}")
col2.metric("Max Risk", f"{df_filtered['Risk_Score'].max()}")
col3.metric("High-Risk Year", f"{df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']}")
col4.metric("Total Orders", f"{df_filtered['Orders'].sum():,}")

# =========================
# FORECAST + RISK VISUALS
# =========================
st.markdown("### 📊 Forecast and Risk Overview")
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
    fig1.update_layout(
        title_x=0.5,
        title_y=0.9,
        title_font=dict(size=18, color="#0f172a"),
        template="plotly_white",
        height=460,
        margin=dict(l=60, r=60, t=100, b=60),
        autosize=True
    )
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

with col2:
    fig2 = px.bar(
        df_filtered,
        x="Year",
        y="Risk_Score",
        color="Risk_Level",
        text="Risk_Score",
        title="Risk Levels by Year",
        color_discrete_map={"Low": "#2ECC71", "Medium": "#F39C12", "High": "#E74C3C"}
    )
    fig2.update_layout(
        title_x=0.5,
        title_y=0.9,
        title_font=dict(size=18, color="#0f172a"),
        template="plotly_white",
        height=460,
        margin=dict(l=60, r=60, t=100, b=60),
        autosize=True
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

# =========================
# ROADMAP (Implementation Timeline)
# =========================
st.markdown("### 🗺️ Implementation Roadmap (2025)")

phases = pd.DataFrame([
    dict(Phase='Planning & Vendor Setup', Start='2025-01-01', Finish='2025-02-28', Category='Planning'),
    dict(Phase='Telemetry Installation', Start='2025-03-01', Finish='2025-04-30', Category='Implementation'),
    dict(Phase='Supplier Integration', Start='2025-05-01', Finish='2025-06-30', Category='Integration'),
    dict(Phase='Pilot & Analytics', Start='2025-07-01', Finish='2025-10-31', Category='Analytics'),
    dict(Phase='Dashboard Deployment', Start='2025-11-01', Finish='2025-12-15', Category='Deployment'),
    dict(Phase='Review & Scale Decision', Start='2025-12-16', Finish='2025-12-31', Category='Review')
])
phases["Start"] = pd.to_datetime(phases["Start"])
phases["Finish"] = pd.to_datetime(phases["Finish"])

colors = {
    'Planning': '#00BFFF',
    'Implementation': '#2ECC71',
    'Integration': '#9B59B6',
    'Analytics': '#F39C12',
    'Deployment': '#1ABC9C',
    'Review': '#E74C3C'
}

fig3 = px.timeline(
    phases,
    x_start="Start",
    x_end="Finish",
    y="Phase",
    color="Category",
    color_discrete_map=colors,
    title="Project Execution Timeline"
)
fig3.update_yaxes(autorange="reversed")
fig3.update_layout(
    height=400,
    title_x=0.5,
    title_y=0.9,
    title_font=dict(size=18, color="#0f172a"),
    margin=dict(l=60, r=60, t=100, b=60),
    template="plotly_white"
)
st.plotly_chart(fig3, use_container_width=True)

# =========================
# RECOMMENDATIONS
# =========================
st.markdown("### 💡 Quick Recommendations")
with st.expander("View Recommendations"):
    st.markdown("""
    - ⚠️ Prioritize supplier oversight in **high-gap years**.
    - Integrate **digital telemetry** for predictive risk monitoring.
    - Automate alerts for suppliers exceeding KPI thresholds.
    - Focus on **Integration & Analytics** phases for maximum ROI.
    """)

# =========================
# FOOTER
# =========================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:13px;'>© 2025 Boeing | Digital Oversight Pilot | Streamlit Dashboard</p>", unsafe_allow_html=True)
