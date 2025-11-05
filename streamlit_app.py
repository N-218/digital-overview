import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Digital Oversight Dashboard", layout="wide")

# Upload CSV
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

# Title
st.title("🔮 Digital Oversight Dashboard")

# Section 1: Data Overview
st.header("🗂️ Data Overview")
st.dataframe(df)

# Section 2: Forecast Chart
st.header("📈 Forecast Chart")
fig1 = px.line(df, x="Year", y="Predicted_Gap", markers=True, title="Forecasted Gap Over Time")
st.plotly_chart(fig1, use_container_width=True)

# Section 3: Risk Chart
st.header("⚠️ Risk Levels by Year")
fig2 = px.bar(df, x="Year", y="Risk_Score", color="Risk_Level", title="Risk Levels by Year")
st.plotly_chart(fig2, use_container_width=True)

# Section 4: KPI Highlights
st.header("🚩 KPI Highlights")
total_gap = df["Predicted_Gap"].sum()
max_risk = df["Risk_Score"].max()
highest_risk_year = df.loc[df["Risk_Score"].idxmax(), "Year"]
st.write("**Total Predicted Gap:**", total_gap)
st.write("**Highest Risk Score:**", max_risk)
st.write("**Year with Highest Risk:**", highest_risk_year)

# Section 5: Recommendations
st.header("✅ Recommendations")
st.markdown("""
- High predicted gaps (2026–2028) indicate a need for earlier supplier oversight.  
- Digital telemetry integration will allow predictive monitoring to reduce these risks.  
- Add automated alerts for suppliers exceeding risk thresholds.  
""")
