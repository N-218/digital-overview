import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Boeing Digital Oversight Dashboard",
    layout="wide",
    page_icon="✈️",
    initial_sidebar_state="expanded"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp { background: #f8fafc; font-family: 'Inter', 'Segoe UI', sans-serif; }

.dashboard-header { background: #003087; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; }

.dashboard-title { color: white; font-size: 2.5rem; font-weight: 700; margin: 0; }
.dashboard-subtitle { color: white; font-size: 1.1rem; margin-top: 0.5rem; }

.section-header { color: #003087; font-size: 1.5rem; font-weight: 600; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0; }

.alert-box { padding: 1rem 1.5rem; border-radius: 8px; margin: 1rem 0; }
.alert-box.critical { background: #fee2e2; border-left: 4px solid #dc2626; }
.alert-box.success { background: #d1fae5; border-left: 4px solid #10b981; }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR: FILE UPLOAD & FILTERS
# =========================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h2 style='color: white; margin: 0; font-size: 1.8rem; letter-spacing: 3px;'>BOEING</h2>
        <p style='color: #94a3b8; font-size: 0.75rem; margin-top: 0.25rem;'>Digital Oversight System</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📂 Data Upload")
    uploaded_file = st.file_uploader("Upload Forecast CSV", type=["csv"], label_visibility="collapsed")
    if uploaded_file is None:
        st.info("👆 Upload your Digital_Oversight_Forecast.csv file to begin")
        st.stop()

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(uploaded_file)
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# Sidebar Filters
with st.sidebar:
    st.markdown("### 🔍 Filters")
    year_range = st.slider(
        "Year Range",
        int(df["Year"].min()),
        int(df["Year"].max()),
        (int(df["Year"].min()), int(df["Year"].max()))
    )
    risk_levels = st.multiselect("Risk Levels", df["Risk_Level"].unique(), default=df["Risk_Level"].unique())

# Apply filters
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]

# =========================
# HEADER
# =========================
st.markdown(f"""
<div class='dashboard-header'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h1 class='dashboard-title'>Digital Oversight Dashboard</h1>
            <p class='dashboard-subtitle'>Supply Chain Intelligence & Risk Management System</p>
        </div>
        <div style='color:white; font-weight:700;'>✈️</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# STRATEGIC KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)
peak_risk = df_filtered['Risk_Score'].max()
total_gap = df_filtered['Predicted_Gap'].sum()
total_orders = df_filtered['Orders'].sum()
critical_year_row = df_filtered.loc[df_filtered['Risk_Score'].idxmax()]

col1.metric("Total Forward Gap (Units)", f"{total_gap:,.0f}", delta=f"{total_gap/total_orders*100:.1f}% of orders")
col2.metric("Peak Oversight Risk Index", peak_risk)
col3.metric("Critical Year Gap", f"{critical_year_row['Predicted_Gap']:,}")
col4.metric("Total Orders Backlog", f"{total_orders:,}")

# =========================
# ALERT
# =========================
high_risk_years = df_filtered[df_filtered['Risk_Level']=='High']['Year'].tolist()
if high_risk_years:
    st.markdown(f"""
    <div class='alert-box critical'>
        ⚠️ High-risk periods detected: {', '.join(map(str, high_risk_years))}
    </div>
    """, unsafe_allow_html=True)

# =========================
# COMBINED GAP ANALYSIS
# =========================
st.markdown("<h2 class='section-header'>📈 Total Gap Analysis (Actual → Forecast)</h2>", unsafe_allow_html=True)
fig_gap = go.Figure()

# Split actual vs forecast
actual_df = df_filtered[df_filtered['Year'] <= 2025]
forecast_df = df_filtered[df_filtered['Year'] > 2025]

fig_gap.add_trace(go.Scatter(
    x=actual_df['Year'], y=actual_df['ProductionGap'],
    mode='lines+markers', name='Actual Gap', line=dict(color='#94a3b8', width=3)
))
fig_gap.add_trace(go.Scatter(
    x=forecast_df['Year'], y=forecast_df['Predicted_Gap'],
    mode='lines+markers', name='Forecast Gap', line=dict(color='#003087', width=3, dash='dash')
))

fig_gap.update_layout(
    xaxis_title="Year", yaxis_title="Gap (Units)",
    template='plotly_white', height=450
)
st.plotly_chart(fig_gap, use_container_width=True, config={'displayModeBar': False})

# =========================
# CORRELATION CHART
# =========================
st.markdown("<h2 class='section-header'>📊 Backlog vs Forward Gap</h2>", unsafe_allow_html=True)
fig_corr = px.scatter(
    df_filtered, x='Orders', y='Predicted_Gap', color='Risk_Level',
    size='Risk_Score', color_discrete_map={'Low':'#10b981','Medium':'#f59e0b','High':'#dc2626'},
    labels={'Orders':'Total Unfilled Backlog','Predicted_Gap':'Total Forward Gap'}, hover_data=['Year']
)
st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})

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
fig_roadmap.add_vline(x=current_date, line_dash="dash", line_color="red", annotation_text="Current Date", annotation_position="top right")
fig_roadmap.update_layout(height=400, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig_roadmap, use_container_width=True, config={'displayModeBar': False})

# =========================
# STRATEGIC RECOMMENDATIONS
# =========================
st.markdown("<h2 class='section-header'>💡 Strategic Recommendations</h2>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='alert-box critical'>
        <h4>🚨 Critical Actions</h4>
        <ul>
            <li>Implement real-time telemetry for high-risk suppliers</li>
            <li>Establish automated alert system for KPI deviations</li>
            <li>Increase oversight frequency during 2026-2027 period</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class='alert-box success'>
        <h4>✅ Quick Wins</h4>
        <ul>
            <li>Deploy dashboard for leadership visibility</li>
            <li>Integrate supplier portals with central monitoring</li>
            <li>Automate weekly risk reports</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='alert-box'>
        <h4>📋 Long-term Strategy</h4>
        <ul>
            <li>Build predictive capacity planning models</li>
            <li>Expand digital oversight to tier-2 suppliers</li>
            <li>Develop supplier performance scorecards</li>
            <li>Invest in AI-powered anomaly detection</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================
# DATA TABLE
# =========================
with st.expander("📊 View Detailed Data Table"):
    st.dataframe(df_filtered.style.background_gradient(subset=['Risk_Score'], cmap='RdYlGn_r'), use_container_width=True, height=400)

# =========================
# FOOTER
# =========================
st.markdown("""
<div style='text-align: center; padding: 2rem 0 1rem 0; border-top: 2px solid #e2e8f0;'>
    <p style='color: #64748b; font-size: 0.875rem; margin: 0;'>
        <strong>Boeing Digital Oversight System</strong> | Version 2.0 | © 2025 The Boeing Company
    </p>
    <p style='color: #94a3b8; font-size: 0.75rem; margin-top: 0.5rem;'>
        Powered by Advanced Analytics & Machine Learning | Last Updated: November 2025
    </p>
</div>
""", unsafe_allow_html=True)

