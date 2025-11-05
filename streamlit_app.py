import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(page_title="Digital Oversight Dashboard", layout="wide")

# Sidebar: CSV upload
st.sidebar.title("Upload Your Data")
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

# =========================
# Section 1: Data Overview
# =========================
st.header("🗂️ Data Overview")
# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Predicted Gap", f"{df_filtered['Predicted_Gap'].sum():.1f}")
col2.metric("Max Risk Score", f"{df_filtered['Risk_Score'].max()}")
col3.metric("Year with Highest Risk", f"{df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']}")
col4.metric("Total Orders", f"{df_filtered['Orders'].sum()}")

# Optional: summary statistics table
st.subheader("Summary Statistics")
summary_df = df_filtered[["PlannedOutput", "ActualOutput", "Orders", "Backlog", "Predicted_Gap"]].describe()
st.dataframe(summary_df.style.background_gradient(cmap="Blues"))

# =========================
# Section 2 & 3: Charts
# =========================
st.header("📊 Forecast & Risk Charts")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Forecast Gap Over Time")
    fig1 = px.line(
        df_filtered,
        x="Year",
        y="Predicted_Gap",
        markers=True,
        color="Risk_Level",
        hover_data=["PlannedOutput", "ActualOutput", "Backlog"],
        title="Forecasted Gap by Year"
    )
    fig1.update_layout(title_x=0.5, template="plotly_white")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Risk Levels")
    fig2 = px.bar(
        df_filtered,
        x="Year",
        y="Risk_Score",
        color="Risk_Level",
        text="Risk_Score",
        title="Risk Scores by Year"
    )
    fig2.update_layout(title_x=0.5, template="plotly_white")
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# Section 4: Recommendations
# =========================
st.header("✅ Recommendations")

# Highlight high gaps dynamically
high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]["Year"].tolist()
if high_gap_years:
    st.markdown(f"- ⚠️ High predicted gaps detected in {', '.join(map(str, high_gap_years))} — prioritize supplier oversight.")
else:
    st.markdown("- ✅ Predicted gaps are within manageable range.")

st.markdown("""
- Integrate digital telemetry for predictive monitoring.  
- Add automated alerts for suppliers exceeding risk thresholds.  
- Focus on years with high Risk Score for proactive intervention.
""")
