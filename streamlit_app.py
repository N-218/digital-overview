import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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
# ENHANCED CUSTOM CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&family=Roboto+Condensed:wght@400;700&display=swap');

/* Global Styles */
.stApp { 
    background: #f0f2f5; 
    font-family: 'Roboto', sans-serif;
}

/* Remove default Streamlit padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Header Section */
.dashboard-header { 
    background: linear-gradient(135deg, #0033A0 0%, #005EB8 100%);
    padding: 2.5rem 3rem; 
    border-radius: 0;
    margin: -2rem -3rem 2rem -3rem;
    box-shadow: 0 4px 12px rgba(0, 51, 160, 0.2);
}

.header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1400px;
    margin: 0 auto;
}

.header-left h1 { 
    color: white; 
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 2.8rem; 
    font-weight: 700; 
    margin: 0;
    letter-spacing: -0.5px;
}

.header-left p { 
    color: #b8d4f0; 
    font-size: 1.15rem; 
    margin-top: 0.5rem;
    font-weight: 400;
}

.boeing-logo {
    font-family: 'Roboto Condensed', sans-serif;
    color: white;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: 8px;
}

/* Section Headers */
.section-header { 
    color: #0033A0; 
    font-family: 'Roboto Condensed', sans-serif;
    font-size: 1.75rem; 
    font-weight: 700; 
    margin: 3rem 0 1.5rem 0; 
    padding-bottom: 0.75rem; 
    border-bottom: 3px solid #0033A0;
    letter-spacing: -0.5px;
}

/* Metric Cards */
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid #0033A0;
    margin-bottom: 1rem;
}

.metric-label {
    font-size: 0.875rem;
    color: #64748b;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-size: 2.25rem;
    color: #0f172a;
    font-weight: 700;
    line-height: 1;
    margin-bottom: 0.5rem;
}

.metric-delta {
    font-size: 0.875rem;
    color: #64748b;
    font-weight: 500;
}

/* Alert Boxes */
.alert-box { 
    padding: 1.5rem; 
    border-radius: 8px; 
    margin: 1.5rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}

.alert-box.critical { 
    background: #fef2f2; 
    border-left: 5px solid #dc2626;
}

.alert-box.warning { 
    background: #fffbeb; 
    border-left: 5px solid #f59e0b;
}

.alert-box.success { 
    background: #f0fdf4; 
    border-left: 5px solid #10b981;
}

.alert-box.info { 
    background: #eff6ff; 
    border-left: 5px solid #3b82f6;
}

.alert-box h4 {
    font-size: 1.1rem;
    font-weight: 600;
    margin-top: 0;
    margin-bottom: 0.75rem;
}

.alert-box ul {
    margin: 0;
    padding-left: 1.5rem;
}

.alert-box li {
    margin-bottom: 0.5rem;
    line-height: 1.6;
    font-size: 0.95rem;
}

/* Risk Distribution */
.risk-item {
    margin-bottom: 1.25rem;
    padding: 1rem;
    background: white;
    border-radius: 6px;
}

.risk-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}

.risk-label {
    font-weight: 600;
    font-size: 1rem;
    color: #0f172a;
}

.risk-count {
    font-weight: 700;
    font-size: 1.1rem;
}

.risk-bar-bg {
    background: #e2e8f0;
    border-radius: 10px;
    height: 12px;
    overflow: hidden;
}

.risk-bar-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 0.3s ease;
}

/* Phase Progress Cards */
.phase-card {
    text-align: center;
    padding: 1.5rem 1rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-top: 3px solid #0033A0;
}

.phase-progress {
    font-size: 2.5rem;
    font-weight: 700;
    color: #0033A0;
    line-height: 1;
}

.phase-label {
    font-size: 0.875rem;
    color: #64748b;
    margin-top: 0.5rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Footer */
.dashboard-footer {
    text-align: center;
    padding: 2.5rem 0 1.5rem 0;
    border-top: 2px solid #e2e8f0;
    margin-top: 3rem;
}

.footer-title {
    color: #0f172a;
    font-size: 0.95rem;
    font-weight: 600;
    margin: 0;
}

.footer-meta {
    color: #94a3b8;
    font-size: 0.8rem;
    margin-top: 0.5rem;
}

/* Data Table Styling */
.dataframe {
    font-size: 0.9rem !important;
}

/* Sidebar Styling */
.css-1d391kg, [data-testid="stSidebar"] {
    background: #1e293b;
}

.css-1d391kg h2, [data-testid="stSidebar"] h2 {
    color: white !important;
}

.css-1d391kg p, [data-testid="stSidebar"] p {
    color: #cbd5e1 !important;
}

/* Chart Container */
.chart-container {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR: FILE UPLOAD & FILTERS
# =========================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 2.5rem 0; border-bottom: 1px solid #334155;'>
        <h2 style='color: white; margin: 0; font-size: 2.2rem; letter-spacing: 6px; font-family: "Roboto Condensed", sans-serif; font-weight: 700;'>BOEING</h2>
        <p style='color: #94a3b8; font-size: 0.8rem; margin-top: 0.5rem; letter-spacing: 1px;'>DIGITAL OVERSIGHT SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📂 Data Upload")
    uploaded_file = st.file_uploader("Upload Forecast CSV", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file is None:
        st.info("👆 Upload your Digital_Oversight_Forecast.csv file to begin analysis")
        st.stop()

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(uploaded_file)
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# Sidebar Filters
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🔍 Filter Controls")
    year_range = st.slider(
        "Year Range", 
        int(df["Year"].min()), 
        int(df["Year"].max()), 
        (int(df["Year"].min()), int(df["Year"].max()))
    )
    risk_levels = st.multiselect(
        "Risk Levels", 
        df["Risk_Level"].unique(), 
        default=df["Risk_Level"].unique()
    )

# Apply filters
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]

# =========================
# HEADER
# =========================
st.markdown("""
<div class='dashboard-header'>
    <div class='header-content'>
        <div class='header-left'>
            <h1>Digital Oversight Dashboard</h1>
            <p>Supply Chain Intelligence & Risk Management System</p>
        </div>
        <div class='boeing-logo'>BOEING</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KEY METRICS
# =========================
col1, col2, col3, col4 = st.columns(4)

total_gap = df_filtered['Predicted_Gap'].sum()
total_orders = df_filtered['Orders'].sum()
avg_orders = df_filtered['Orders'].mean()
high_risk_count = len(df_filtered[df_filtered['Risk_Level'] == 'High'])
critical_year_row = df_filtered.loc[df_filtered['Risk_Score'].idxmax()]

with col1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Total Predicted Gap</div>
        <div class='metric-value'>{total_gap:,.0f}</div>
        <div class='metric-delta'>{(total_gap/total_orders*100):.1f}% of total orders</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>High-Risk Periods</div>
        <div class='metric-value'>{high_risk_count}</div>
        <div class='metric-delta'>{(high_risk_count/len(df_filtered)*100):.0f}% of timeline</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Critical Year</div>
        <div class='metric-value'>{critical_year_row['Year']}</div>
        <div class='metric-delta'>Gap: {critical_year_row['Predicted_Gap']:,} units</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Total Orders</div>
        <div class='metric-value'>{total_orders:,}</div>
        <div class='metric-delta'>Average: {avg_orders:.0f} per year</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# CRITICAL ALERT
# =========================
high_risk_years = df_filtered[df_filtered['Risk_Level'] == 'High']['Year'].tolist()
if high_risk_years:
    st.markdown(f"""
    <div class='alert-box critical'>
        <h4>⚠️ CRITICAL ALERT: High-Risk Periods Detected</h4>
        <p style='margin: 0; font-size: 1rem; line-height: 1.6;'>
            <strong>Affected Years:</strong> {', '.join(map(str, high_risk_years))}<br>
            <strong>Action Required:</strong> Immediate supplier oversight and capacity planning review needed.
        </p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# PRODUCTION ANALYSIS
# =========================
st.markdown("<h2 class='section-header'>PRODUCTION ANALYSIS & FORECASTING</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=df_filtered['Year'], 
        y=df_filtered['ProductionGap'], 
        name='Actual Gap',
        mode='lines+markers',
        line=dict(color='#94a3b8', width=3),
        marker=dict(size=8)
    ))
    
    fig1.add_trace(go.Scatter(
        x=df_filtered['Year'], 
        y=df_filtered['Predicted_Gap'], 
        name='Predicted Gap',
        mode='lines+markers',
        line=dict(color='#0033A0', width=4),
        marker=dict(size=10, symbol='diamond')
    ))
    
    fig1.update_layout(
        title=dict(text='Production Gap: Actual vs Predicted', font=dict(size=16, weight=600)),
        xaxis_title='Year',
        yaxis_title='Gap (Units)',
        template='plotly_white',
        height=450,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("#### Risk Level Distribution")
    
    risk_counts = df_filtered['Risk_Level'].value_counts()
    
    for level in ['High', 'Medium', 'Low']:
        if level in risk_counts.index:
            count = risk_counts[level]
            perc = (count / len(df_filtered)) * 100
            color = {'High': '#dc2626', 'Medium': '#f59e0b', 'Low': '#10b981'}[level]
            
            st.markdown(f"""
            <div class='risk-item'>
                <div class='risk-header'>
                    <span class='risk-label'>{level} Risk</span>
                    <span class='risk-count' style='color:{color}'>{count} ({perc:.0f}%)</span>
                </div>
                <div class='risk-bar-bg'>
                    <div class='risk-bar-fill' style='width:{perc}%; background:{color};'></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ORDERS vs GAP CORRELATION
# =========================
st.markdown("<h2 class='section-header'>ORDERS & GAP CORRELATION ANALYSIS</h2>", unsafe_allow_html=True)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
fig2 = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Orders vs Predicted Gap Scatter', 'Year-over-Year Risk Progression'),
    specs=[[{"secondary_y": False}, {"type": "bar"}]]
)

fig2.add_trace(go.Scatter(
    x=df_filtered['Orders'],
    y=df_filtered['Predicted_Gap'],
    mode='markers',
    marker=dict(
        size=df_filtered['Risk_Score']*12,
        color=df_filtered['Risk_Score'],
        colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#dc2626']],
        showscale=True,
        colorbar=dict(title="Risk Level", x=0.46)
    ),
    text=df_filtered['Year'],
    hovertemplate='<b>Year %{text}</b><br>Orders: %{x:,}<br>Predicted Gap: %{y:,}<extra></extra>',
    name='Year Data'
), row=1, col=1)

colors_map = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#dc2626'}
fig2.add_trace(go.Bar(
    x=df_filtered['Year'],
    y=df_filtered['Risk_Score'],
    marker_color=[colors_map[l] for l in df_filtered['Risk_Level']],
    text=df_filtered['Risk_Level'],
    textposition='outside',
    name='Risk Level',
    hovertemplate='<b>Year %{x}</b><br>Risk: %{text}<extra></extra>'
), row=1, col=2)

fig2.update_xaxes(title_text="Orders", row=1, col=1)
fig2.update_yaxes(title_text="Predicted Gap", row=1, col=1)
fig2.update_xaxes(title_text="Year", row=1, col=2)
fig2.update_yaxes(title_text="Risk Score", row=1, col=2)

fig2.update_layout(
    height=450,
    showlegend=False,
    template='plotly_white',
    hovermode='closest'
)

st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# IMPLEMENTATION ROADMAP
# =========================
st.markdown("<h2 class='section-header'>IMPLEMENTATION ROADMAP 2025</h2>", unsafe_allow_html=True)

st.markdown("<div class='chart-container'>", unsafe_allow_html=True)

phases = pd.DataFrame([
    dict(Phase='Phase 1: Planning & Vendor Setup', Start='2025-01-01', Finish='2025-02-28', Category='Planning', Progress=100),
    dict(Phase='Phase 2: Telemetry Installation', Start='2025-03-01', Finish='2025-04-30', Category='Implementation', Progress=75),
    dict(Phase='Phase 3: Supplier Integration', Start='2025-05-01', Finish='2025-06-30', Category='Integration', Progress=45),
    dict(Phase='Phase 4: Pilot & Analytics', Start='2025-07-01', Finish='2025-10-31', Category='Analytics', Progress=20),
    dict(Phase='Phase 5: Dashboard Deployment', Start='2025-11-01', Finish='2025-12-15', Category='Deployment', Progress=0),
    dict(Phase='Phase 6: Review & Scale Decision', Start='2025-12-16', Finish='2025-12-31', Category='Review', Progress=0)
])

phases["Start"] = pd.to_datetime(phases["Start"])
phases["Finish"] = pd.to_datetime(phases["Finish"])

colors = {
    'Planning': '#0033A0',
    'Implementation': '#005EB8',
    'Integration': '#2563eb',
    'Analytics': '#3b82f6',
    'Deployment': '#60a5fa',
    'Review': '#93c5fd'
}

fig3 = px.timeline(
    phases,
    x_start="Start",
    x_end="Finish",
    y="Phase",
    color="Category",
    color_discrete_map=colors
)

fig3.update_yaxes(autorange="reversed")
fig3.update_layout(
    height=400,
    title=dict(text='Project Timeline', font=dict(size=16, weight=600)),
    template='plotly_white',
    xaxis_title="Timeline",
    yaxis_title=""
)

st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
st.markdown("</div>", unsafe_allow_html=True)

# Phase Progress Cards
cols = st.columns(6)
for col, row in zip(cols, phases.itertuples()):
    with col:
        st.markdown(f"""
        <div class='phase-card'>
            <div class='phase-progress'>{row.Progress}%</div>
            <div class='phase-label'>{row.Category}</div>
        </div>
        """, unsafe_allow_html=True)

# =========================
# STRATEGIC RECOMMENDATIONS
# =========================
st.markdown("<h2 class='section-header'>STRATEGIC RECOMMENDATIONS</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='alert-box critical'>
        <h4>🚨 Critical Actions Required</h4>
        <ul>
            <li>Implement real-time telemetry systems for all high-risk tier-1 suppliers</li>
            <li>Establish automated alert protocols for KPI deviation thresholds</li>
            <li>Increase oversight frequency and audit schedules for 2026-2027 period</li>
            <li>Deploy contingency supplier identification and qualification process</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='alert-box success'>
        <h4>✅ Quick Win Initiatives</h4>
        <ul>
            <li>Deploy executive dashboard for real-time leadership visibility</li>
            <li>Integrate supplier portals with central monitoring infrastructure</li>
            <li>Automate weekly risk assessment and distribution reports</li>
            <li>Establish cross-functional risk review committee</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='alert-box info'>
        <h4>📋 Long-Term Strategic Initiatives</h4>
        <ul>
            <li>Develop ML-powered predictive capacity planning models</li>
            <li>Expand digital oversight framework to tier-2 and tier-3 suppliers</li>
            <li>Create comprehensive supplier performance scorecard system</li>
            <li>Invest in AI-powered anomaly detection and early warning systems</li>
            <li>Build supplier resilience index and diversification metrics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# =========================
# DATA TABLE
# =========================
st.markdown("<h2 class='section-header'>DETAILED DATA TABLE</h2>", unsafe_allow_html=True)

with st.expander("📊 View Complete Dataset", expanded=False):
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.dataframe(
        df_filtered.style.background_gradient(subset=['Risk_Score'], cmap='RdYlGn_r'),
        use_container_width=True,
        height=400
    )
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class='dashboard-footer'>
    <p class='footer-title'>BOEING DIGITAL OVERSIGHT SYSTEM | VERSION 2.0</p>
    <p class='footer-meta'>
        © 2025 The Boeing Company | Powered by Advanced Analytics & Machine Learning<br>
        Last Updated: November 2025 | Confidential & Proprietary
    </p>
</div>
""", unsafe_allow_html=True)
