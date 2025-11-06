import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Boeing Digital Oversight Dashboard",
    page_icon="✈️",
    layout="wide"
)

# =========================
# Styling: Boeing Colors + Logo
# =========================
st.markdown("""
<style>
    /* App background */
    .stApp {
        background: linear-gradient(to bottom right, #f0f3f7, #ffffff);
        font-family: 'Segoe UI', sans-serif;
    }
    /* Boeing logo watermark */
    .stApp::before {
        content: "";
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/3/36/Boeing_full_logo.svg");
        background-size: 15%;
        background-repeat: no-repeat;
        background-position: top right;
        opacity: 0.08;
        position: fixed;
        top: 0; right: 0; bottom: 0; left: 0;
        z-index: 0;
    }
    /* Headers */
    h1, h2, h3 {
        font-family: 'Segoe UI', sans-serif;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# Sidebar: Upload & Filters
# =========================
st.sidebar.title("📂 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload Digital_Oversight_Forecast.csv", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload your CSV to view the dashboard.")
    st.stop()

# Map risk levels to numeric scores
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# Filters
st.sidebar.header("🔍 Filters")
year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)
risk_levels = st.sidebar.multiselect(
    "Select Risk Levels",
    options=df["Risk_Level"].unique(),
    default=df["Risk_Level"].unique()
)

# Apply filters
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]

# =========================
# Header
# =========================
st.markdown("""
<div style='text-align: center;'>
<h1 style='color:#0a3d62; font-size:36px;'>✈️ Boeing Digital Oversight Dashboard</h1>
<p style='font-size:16px; color:#34495e;'>Forecast | Risk | Implementation Roadmap</p>
<hr style='width:50%; border:1px solid #dcdde1; margin:auto'>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI Metrics
# =========================
st.markdown("### 🚩 Key Insights")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Predicted Gap", f"{df_filtered['Predicted_Gap'].sum():,.0f}")
col2.metric("Max Risk Score", f"{df_filtered['Risk_Score'].max()}")
col3.metric("High-Risk Year", f"{df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']}")
col4.metric("Total Orders", f"{df_filtered['Orders'].sum():,}")

st.markdown("---")

# =========================
# Forecast & Risk Charts
# =========================
st.markdown("### 📊 Forecast & Risk Overview")
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(
        df_filtered,
        x="Year",
        y=["Predicted_Gap", "ProductionGap"] if "ProductionGap" in df.columns else ["Predicted_Gap"],
        markers=True,
        labels={"value": "Gap", "variable": "Type"},
        title="Production Gap Forecast",
        color_discrete_sequence=["#1E90FF", "#E74C3C"]
    )
    fig1.update_layout(height=350, title_x=0.5, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

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
    fig2.update_layout(height=350, title_x=0.5, template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# =========================
# Implementation Roadmap
# =========================
st.markdown("### 🗺️ Implementation Roadmap (2025)")
phases = pd.DataFrame([
    dict(Task='Planning & Vendor Setup', Start='2025-01-01', Finish='2025-02-28', Resource='Planning'),
    dict(Task='Telemetry Installation', Start='2025-03-01', Finish='2025-04-30', Resource='Implementation'),
    dict(Task='Supplier Integration', Start='2025-05-01', Finish='2025-06-30', Resource='Integration'),
    dict(Task='Pilot & Analytics', Start='2025-07-01', Finish='2025-12-31', Resource='Analytics'),
    dict(Task='Dashboard Deployment', Start='2025-07-01', Finish='2025-12-31', Resource='Dashboard'),
    dict(Task='Review & Scale Decision', Start='2025-12-31', Finish='2025-12-31', Resource='Review')
])
phases["Start"] = pd.to_datetime(phases["Start"])
phases["Finish"] = pd.to_datetime(phases["Finish"])

colors = {
    'Planning': '#00BFFF',
    'Implementation': '#2ECC71',
    'Integration': '#9B59B6',
    'Analytics': '#F39C12',
    'Dashboard': '#1ABC9C',
    'Review': '#E74C3C'
}

fig3 = px.timeline(
    phases,
    x_start="Start",
    x_end="Finish",
    y="Task",
    color="Resource",
    color_discrete_map=colors,
)
fig3.update_yaxes(autorange="reversed")
fig3.update_layout(height=300, title="Roadmap Timeline", title_x=0.5, template="plotly_white", margin=dict(l=10,r=10,t=30,b=10))
st.plotly_chart(fig3, use_container_width=True)

# =========================
# Recommendations
# =========================
st.markdown("### 💡 Recommendations")
with st.expander("View Recommendations"):
    high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]["Year"].tolist()
    if high_gap_years:
        st.markdown(f"- ⚠️ High predicted gaps detected in {', '.join(map(str, high_gap_years))} — prioritize supplier oversight.")
    else:
        st.markdown("- ✅ Predicted gaps are within manageable range.")
    
    st.markdown("""
    - Integrate digital telemetry for predictive monitoring.
    - Add automated alerts for suppliers exceeding risk thresholds.
    - Focus on years with high Risk Score for proactive intervention.
    - Emphasize Integration & Analytics phases for highest ROI.
    """)

# =========================
# Footer
# =========================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:13px;'>© 2025 Boeing | Digital Oversight Dashboard</p>", unsafe_allow_html=True)
