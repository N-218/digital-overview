import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(page_title="Boeing Digital Oversight Dashboard",
                   layout="wide", page_icon="✈️")

# =========================
# STYLES
# =========================
st.markdown("""
<style>
.stApp { background: #f8fafc; font-family: 'Inter', sans-serif; }
.dashboard-header { background:#003087; padding:1.5rem 1rem; border-radius:12px; margin-bottom:1.5rem; color:white; }
.dashboard-title { color:white; font-size:2rem; font-weight:700; margin:0; }
.dashboard-subtitle { color:white; font-size:1rem; margin-top:0.25rem; }
.metric-card { background:white; padding:1rem; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.08); }
.metric-value { color:#003087; font-size:1.75rem; font-weight:700; }
.metric-label { color:#64748b; font-size:0.875rem; font-weight:500; }
.section-header { color:#003087; font-size:1.5rem; font-weight:600; margin:1.5rem 0 0.5rem 0; border-bottom:2px solid #e2e8f0; }
.alert-box { padding:1rem; border-radius:8px; margin:0.5rem 0; }
.alert-box.critical { background:#fee2e2; border-left:4px solid #dc2626; }
.alert-box.success { background:#d1fae5; border-left:4px solid #10b981; }
.alert-box.info { background:#fef3c7; border-left:4px solid #f59e0b; }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("<h2 style='color:white'>BOEING</h2>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload Forecast CSV", type=["csv"])
    if uploaded_file is None:
        st.info("👆 Upload your Digital_Oversight_Forecast.csv file to begin")
        st.stop()

# Load Data
df = pd.read_csv(uploaded_file)
risk_mapping = {"Low":1, "Medium":2, "High":3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# Sidebar Filters
with st.sidebar:
    st.markdown("### 🔍 Filters")
    year_range = st.slider("Year Range", int(df["Year"].min()), int(df["Year"].max()), (int(df["Year"].min()), int(df["Year"].max())))
    risk_levels = st.multiselect("Risk Levels", df["Risk_Level"].unique(), default=df["Risk_Level"].unique())

# Filter Data
df_filtered = df[(df["Year"]>=year_range[0]) & (df["Year"]<=year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]

# =========================
# HEADER
# =========================
st.markdown(f"""
<div class='dashboard-header'>
    <div style='display:flex; justify-content:space-between; align-items:center;'>
        <div>
            <h1 class='dashboard-title'>Digital Oversight Dashboard</h1>
            <p class='dashboard-subtitle'>Supply Chain Intelligence & Risk Management System</p>
        </div>
        <div>✈️</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI METRICS
# =========================
col1,col2,col3,col4 = st.columns(4)
with col1:
    total_gap = df_filtered['Predicted_Gap'].sum()
    st.metric("Peak Oversight Risk Index", f"{total_gap:,.0f}", delta=f"{((total_gap/df_filtered['Orders'].sum())*100):.1f}% of orders")
with col2:
    high_risk_count = len(df_filtered[df_filtered['Risk_Level']=='High'])
    st.metric("High-Risk Periods", high_risk_count, delta=f"{(high_risk_count/len(df_filtered)*100):.0f}% of timeline")
with col3:
    critical_year = df_filtered.loc[df_filtered['Risk_Score'].idxmax(),'Year']
    critical_gap = df_filtered.loc[df_filtered['Risk_Score'].idxmax(),'Predicted_Gap']
    st.metric("Critical Year", critical_year, delta=f"Gap: {critical_gap:,.0f}")
with col4:
    total_orders = df_filtered['Orders'].sum()
    avg_orders = df_filtered['Orders'].mean()
    st.metric("Total Orders", f"{total_orders:,.0f}", delta=f"Avg: {avg_orders:,.0f}/yr")

# Risk Alert
high_risk_years = df_filtered[df_filtered['Risk_Level']=='High']['Year'].tolist()
if high_risk_years:
    st.markdown(f"<div class='alert-box critical'>⚠️ High-risk years: {', '.join(map(str,high_risk_years))}</div>", unsafe_allow_html=True)

# =========================
# TOTAL GAP CHART
# =========================
st.markdown("<h2 class='section-header'>📈 Total Gap Analysis</h2>", unsafe_allow_html=True)
df_sorted = df_filtered.sort_values('Year')
fig_gap = go.Figure()
fig_gap.add_trace(go.Scatter(x=df_sorted['Year'], y=df_sorted['ProductionGap'], mode='lines+markers', name='Actual', line=dict(color='#94a3b8')))
fig_gap.add_trace(go.Scatter(x=df_sorted['Year'], y=df_sorted['Predicted_Gap'], mode='lines+markers', name='Forecast', line=dict(color='#003087', dash='dot')))
fig_gap.update_layout(height=400, template='plotly_white', title="Production Gap: Actual vs Forecast")
st.plotly_chart(fig_gap, use_container_width=True)

# =========================
# CORRELATION CHART
# =========================
st.markdown("<h2 class='section-header'>📊 Backlog vs Forward Gap</h2>", unsafe_allow_html=True)
fig_corr = px.scatter(df_filtered, x='Orders', y='Predicted_Gap', color='Risk_Level', size='Risk_Score', hover_data=['Year'])
st.plotly_chart(fig_corr, use_container_width=True)

# =========================
# ROADMAP
# =========================
st.markdown("<h2 class='section-header'>🗺️ Implementation Roadmap 2025</h2>", unsafe_allow_html=True)
phases = pd.DataFrame([
    dict(Phase='Planning & Vendor Setup', Start='2025-01-01', Finish='2025-02-28', Category='Planning', Progress=100),
    dict(Phase='Telemetry Installation', Start='2025-03-01', Finish='2025-04-30', Category='Implementation', Progress=75),
    dict(Phase='Supplier Integration', Start='2025-05-01', Finish='2025-06-30', Category='Integration', Progress=45),
    dict(Phase='Pilot & Analytics', Start='2025-07-01', Finish='2025-10-31', Category='Analytics', Progress=20),
    dict(Phase='Dashboard Deployment', Start='2025-11-01', Finish='2025-12-15', Category='Deployment', Progress=0),
    dict(Phase='Review & Scale Decision', Start='2025-12-16', Finish='2025-12-31', Category='Review', Progress=0)
])
phases["Start"] = pd.to_datetime(phases["Start"])
phases["Finish"] = pd.to_datetime(phases["Finish"])
colors = {'Planning':'#003087','Implementation':'#0052CC','Integration':'#2563eb','Analytics':'#3b82f6','Deployment':'#60a5fa','Review':'#93c5fd'}

fig_roadmap = px.timeline(phases, x_start="Start", x_end="Finish", y="Phase", color="Category", color_discrete_map=colors)
fig_roadmap.update_yaxes(autorange="reversed")

current_date = pd.to_datetime("2025-11-01")
fig_roadmap.add_vline(x=current_date, line_dash="dash", line_color="red")
fig_roadmap.add_annotation(x=current_date, y=-0.5, text="Current Date", showarrow=True, arrowhead=2, ax=0, ay=-40)

fig_roadmap.update_layout(height=300, margin=dict(l=20,r=20,t=30,b=20))
st.plotly_chart(fig_roadmap, use_container_width=True)

# =========================
# STRATEGIC RECOMMENDATIONS
# =========================
st.markdown("<h2 class='section-header'>💡 Strategic Recommendations</h2>", unsafe_allow_html=True)
col1,col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class='alert-box critical'>🚨 Critical Actions
        <ul>
            <li>Real-time telemetry for high-risk suppliers</li>
            <li>Automated KPI deviation alerts</li>
            <li>Increase oversight 2026-2027</li>
        </ul>
    </div>
    <div class='alert-box success'>✅ Quick Wins
        <ul>
            <li>Deploy dashboard for leadership</li>
            <li>Integrate supplier portals</li>
            <li>Automate weekly risk reports</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='alert-box'>📋 Long-term Strategy
        <ul>
            <li>Predictive capacity planning</li>
            <li>Extend oversight to tier-2 suppliers</li>
            <li>Supplier performance scorecards</li>
            <li>AI anomaly detection</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================
# DATA TABLE
# =========================
with st.expander("📊 View Detailed Data Table"):
    st.dataframe(df_filtered, use_container_width=True, height=250)

# =========================
# FOOTER
# =========================
st.markdown("""
<div style='text-align:center; padding:1rem 0; border-top:2px solid #e2e8f0; font-size:0.8rem; color:#64748b;'>
    <strong>Boeing Digital Oversight System</strong> | Version 2.0 | © 2025 The Boeing Company
    <br>Powered by Advanced Analytics & Machine Learning
</div>
""", unsafe_allow_html=True)
