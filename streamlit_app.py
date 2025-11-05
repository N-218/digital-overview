import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Digital Oversight Dashboard", layout="wide")

# Sidebar: CSV upload
st.sidebar.title("Upload your data")
uploaded_file = st.sidebar.file_uploader("Upload Digital_Oversight_Forecast.csv", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload your CSV in the sidebar to see the dashboard.")
    st.stop()

# Map risk levels to numeric scores
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# Sidebar Filters
st.sidebar.header("Filters")
year_range = st.sidebar.slider(
    "Select Year Range", int(df["Year"].min()), int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)
risk_levels = st.sidebar.multiselect(
    "Select Risk Level(s)", options=df["Risk_Level"].unique(), default=df["Risk_Level"].unique()
)

# Apply filters
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]

# Title
st.title("🔮 Digital Oversight Dashboard")

# KPI Highlights
st.header("🚩 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Predicted Gap", f"{df_filtered['Predicted_Gap'].sum():.1f}")
col2.metric("Highest Risk Score", f"{df_filtered['Risk_Score'].max()}")
col3.metric(
    "Year with Highest Risk",
    f"{df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']}"
)

# Forecast Gap Line Chart
st.header("📈 Forecast Gap Over Time")
fig1 = px.line(
    df_filtered,
    x="Year",
    y="Predicted_Gap",
    markers=True,
    color="Risk_Level",
    hover_data=["PlannedOutput", "ActualOutput", "Backlog"]
)
st.plotly_chart(fig1, use_container_width=True)

# Risk Level Bar Chart
st.header("⚠️ Risk Levels")
fig2 = px.bar(
    df_filtered,
    x="Year",
    y="Risk_Score",
    color="Risk_Level",
    text="Risk_Score",
    title="Risk Scores by Year"
)
st.plotly_chart(fig2, use_container_width=True)

# Dynamic Recommendations
st.header("✅ Recommendations")
if df_filtered["Predicted_Gap"].max() > 300:
    st.markdown("- ⚠️ High predicted gaps detected — prioritize supplier oversight.")
else:
    st.markdown("- ✅ Predicted gaps are within manageable range.")

st.markdown("""
- Integrate digital telemetry for predictive monitoring.  
- Add automated alerts for suppliers exceeding risk thresholds.  
- Focus on years with high Risk Score for proactive intervention.
""")
