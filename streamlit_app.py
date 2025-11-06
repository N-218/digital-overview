import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio

# ================================
# 🎯 PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Boeing Digital Oversight Dashboard",
    layout="wide",
    page_icon="✈️",
)

st.title("✈️ Boeing Digital Production Oversight Pilot Dashboard")
st.markdown("#### Transparency, Predictability, and Speed — Where We Need It Most")

# ================================
# 📊 DATA LOADING
# ================================
data = pd.DataFrame({
    "Year": [2021, 2022, 2023, 2024, 2025],
    "PlannedOutput": [264, 372, 456, 456, 456],
    "ActualOutput": [263, 387, 396, 265, 45],
    "ProductionGap": [1, -15, 60, 191, 411],
    "Predicted_Gap": [-75.6, 27.0, 129.6, 232.2, 334.8]
})

# ================================
# 📈 FORECAST CHART
# ================================
st.subheader("📈 Forecast: Production Gaps (Actual vs Predicted)")

fig1 = px.line(
    data,
    x="Year",
    y=["ProductionGap", "Predicted_Gap"],
    markers=True,
    labels={"value": "Gap", "variable": "Type"},
    title="Production Gap vs Predicted Future Trends"
)
fig1.update_layout(template="plotly_dark")
st.plotly_chart(fig1, use_container_width=True)

# ================================
# ⚠️ RISK CHART
# ================================
st.subheader("⚠️ Risk Visualization")

risk_levels = []
for g in data["Predicted_Gap"]:
    if g < 100:
        risk_levels.append("Low")
    elif g < 250:
        risk_levels.append("Medium")
    else:
        risk_levels.append("High")

data["Risk_Level"] = risk_levels

fig2 = px.bar(
    data,
    x="Year",
    y="Predicted_Gap",
    color="Risk_Level",
    color_discrete_map={"Low": "green", "Medium": "orange", "High": "red"},
    title="Predicted Production Gap – Risk Level by Year"
)
fig2.update_layout(template="plotly_dark")
st.plotly_chart(fig2, use_container_width=True)

# ================================
# 🚀 IMPLEMENTATION ROADMAP
# ================================
st.subheader("🚀 Implementation Roadmap – Digital Oversight Pilot")

phases = pd.DataFrame([
    dict(Phase='Phase 1: Project Planning & Vendor Setup', Start='2025-01-01', Finish='2025-02-28', Category='Planning'),
    dict(Phase='Phase 2: Shop-Floor Telemetry Installation', Start='2025-03-01', Finish='2025-04-30', Category='Implementation'),
    dict(Phase='Phase 3: Supplier Telemetry Integration', Start='2025-05-01', Finish='2025-06-30', Category='Integration'),
    dict(Phase='Phase 4: Pilot Operations & Predictive Analytics', Start='2025-07-01', Finish='2025-12-31', Category='Analytics'),
    dict(Phase='Phase 5: Unified KPI Dashboards Deployment', Start='2025-07-01', Finish='2025-12-31', Category='Dashboard'),
    dict(Phase='Phase 6: Results Review & Scale-Up Decision', Start='2025-12-31', Finish='2025-12-31', Category='Review')
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
    y="Phase",
    color="Category",
    color_discrete_map=colors,
    title="Project Implementation Roadmap (2025)"
)
fig3.update_yaxes(autorange="reversed")
fig3.update_layout(template="plotly_dark", height=600)
st.plotly_chart(fig3, use_container_width=True)

# ================================
# 🧭 KPI SUMMARY
# ================================
st.subheader("📊 KPI Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Average Gap", f"{data['ProductionGap'].mean():.1f}")
col2.metric("Highest Risk Year", data.loc[data['Predicted_Gap'].idxmax(), 'Year'])
col3.metric("Goal", "10–20% Reduction in Delay")

# ================================
# 💬 RECOMMENDATIONS
# ================================
st.subheader("💬 Strategic Insights")
st.markdown("""
**🔹 Observations:**
- Production Gaps are increasing toward 2025.
- Forecast indicates higher risk levels from 2024–2025.
- Predictive analytics & telemetry can help anticipate delays earlier.

**🔹 Recommendations:**
1. Accelerate supplier telemetry integration (Phase 3).
2. Enhance data visibility across Renton and key suppliers.
3. Deploy predictive models in real-time dashboards by Q4 2025.

> “Digital oversight creates transparency, predictability, and speed — where we need it most.”
""")
