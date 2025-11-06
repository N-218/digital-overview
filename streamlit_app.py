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
# ENHANCED CUSTOM CSS - BOEING PROFESSIONAL THEME
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&family=Roboto+Condensed:wght@400;700&display=swap');

.stApp { background: #E8EDF2; font-family: 'Roboto', sans-serif; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

.dashboard-header { 
    background: linear-gradient(135deg, #001F5B 0%, #0039A6 50%, #005EB8 100%);
    padding: 2.5rem 3rem; border-radius: 0; margin: -2rem -3rem 2rem -3rem;
    box-shadow: 0 6px 20px rgba(0, 31, 91, 0.3);
}

.header-content { display: flex; justify-content: space-between; align-items: center; max-width: 1400px; margin: 0 auto; }
.header-left h1 { color: white; font-family: 'Roboto Condensed', sans-serif; font-size: 2.8rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
.header-left p { color: #C5D9F1; font-size: 1.15rem; margin-top: 0.5rem; font-weight: 400; }
.boeing-logo { font-family: 'Roboto Condensed', sans-serif; color: white; font-size: 3rem; font-weight: 700; letter-spacing: 8px; }

.section-header { color: #001F5B; font-family: 'Roboto Condensed', sans-serif; font-size: 1.75rem; font-weight: 700; 
                  margin: 3rem 0 1.5rem 0; padding-bottom: 0.75rem; border-bottom: 3px solid #0039A6; letter-spacing: -0.5px; }

.metric-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,31,91,0.1);
               border-left: 4px solid #0039A6; margin-bottom: 1rem; transition: all 0.3s ease; cursor: pointer; }
.metric-card:hover { box-shadow: 0 6px 20px rgba(0, 57, 166, 0.25); transform: translateY(-2px); border-left-color: #005EB8; }
.metric-label { font-size: 0.875rem; color: #5B6B7C; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }
.metric-value { font-size: 2.25rem; color: #001F5B; font-weight: 700; line-height: 1; margin-bottom: 0.5rem; }
.metric-delta { font-size: 0.875rem; color: #5B6B7C; font-weight: 500; }

.alert-box { padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0; box-shadow: 0 2px 12px rgba(0,31,91,0.08); }
.alert-box.critical { background: #FFF5F5; border-left: 5px solid #C81E1E; }
.alert-box.success { background: #F0F9F4; border-left: 5px solid #0B8043; }
.alert-box.info { background: #EBF4FF; border-left: 5px solid #0039A6; }
.alert-box h4 { font-size: 1.1rem; font-weight: 600; margin-top: 0; margin-bottom: 0.75rem; color: #001F5B; }
.alert-box ul { margin: 0; padding-left: 1.5rem; }
.alert-box li { margin-bottom: 0.5rem; line-height: 1.6; font-size: 0.95rem; color: #1F2937; }

.risk-item { margin-bottom: 1.25rem; padding: 1rem; background: white; border-radius: 6px; box-shadow: 0 1px 4px rgba(0,31,91,0.08); }
.risk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.risk-label { font-weight: 600; font-size: 1rem; color: #001F5B; }
.risk-count { font-weight: 700; font-size: 1.1rem; }
.risk-bar-bg { background: #D4DEE7; border-radius: 10px; height: 12px; overflow: hidden; }
.risk-bar-fill { height: 100%; border-radius: 10px; transition: width 0.3s ease; }

.phase-card { text-align: center; padding: 1.5rem 1rem; background: white; border-radius: 8px;
              box-shadow: 0 2px 12px rgba(0,31,91,0.1); border-top: 3px solid #0039A6; transition: all 0.3s ease; }
.phase-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(0, 57, 166, 0.25); }
.phase-progress { font-size: 2.5rem; font-weight: 700; color: #0039A6; line-height: 1; }
.phase-label { font-size: 0.875rem; color: #5B6B7C; margin-top: 0.5rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }

.dashboard-footer { text-align: center; padding: 2.5rem 0 1.5rem 0; border-top: 2px solid #D4DEE7; margin-top: 3rem; }
.footer-title { color: #001F5B; font-size: 0.95rem; font-weight: 600; margin: 0; }
.footer-meta { color: #5B6B7C; font-size: 0.8rem; margin-top: 0.5rem; }

.chart-container { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 12px rgba(0,31,91,0.1); margin-bottom: 1.5rem; }

.stButton>button { background: linear-gradient(135deg, #001F5B 0%, #0039A6 100%); color: white; border: none; border-radius: 6px; padding: 0.5rem 1.5rem; 
                   font-weight: 600; transition: all 0.3s ease; }
.stButton>button:hover { background: linear-gradient(135deg, #0039A6 0%, #005EB8 100%); box-shadow: 0 6px 16px rgba(0, 57, 166, 0.4); transform: translateY(-1px); }

.stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
.stTabs [data-baseweb="tab"] { background-color: white; border-radius: 8px 8px 0 0; padding: 1rem 2rem; font-weight: 600; 
                                 box-shadow: 0 2px 8px rgba(0,31,91,0.08); }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #001F5B 0%, #0039A6 100%); color: white; }
</style>
""", unsafe_allow_html=True)

# =========================
# EMBEDDED DATASET
# =========================
data = {
    'Year': [2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028],
    'PlannedOutput': [264, 372, 456, 456, 456, 0, 0, 0],
    'ActualOutput': [263, 387, 396, 265, 455, 0, 0, 0],
    'Orders': [395, 626, 1075, 236, 488, 0, 0, 0],
    'Backlog': [341, 365, 433, 430, 164, 0, 0, 0],
    'ProductionGap': [41, 3, 32, 319, 411, 0, 0, 0],
    'Backlog_Change_Pct': [0, -1, 6, -0.007, 0.119, 0, 0, 0],
    'NetLoss': [-45, -150.07, 600.186, -476.9, -724.3, 0, 0, 0],
    'ForwardLosses': [9.2, -54, -63, -217, -585, 0, 0, 0],
    'ExcessCapacityCost': [-227.3, 600, 300, -70, -55, 0, 0, 0],
    'Risk_Level': ['Low', 'Low', 'Medium', 'Medium', 'High', 'High', 'High', 'High'],
    'Predicted_Gap': [-75.6, 27, 129.6, 232.2, 334.8, 437.4, 540, 642.6]
}

df_embedded = pd.DataFrame(data)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0 2.5rem 0; border-bottom: 2px solid #0039A6;'>
        <h2 style='color: #0039A6; margin: 0; font-size: 2.2rem; letter-spacing: 6px; font-family: "Roboto Condensed", sans-serif; font-weight: 700;'>BOEING</h2>
        <p style='color: #5B6B7C; font-size: 0.8rem; margin-top: 0.5rem; letter-spacing: 1px; font-weight: 500;'>DIGITAL OVERSIGHT SYSTEM</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📂 Data Source")
    uploaded_file = st.file_uploader("Upload Custom CSV (Optional)", type=["csv"], label_visibility="collapsed")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("✅ Custom data loaded")
    else:
        df = df_embedded.copy()
        st.info("📊 Using embedded dataset")

risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# =========================
# INTERACTIVE FILTERS
# =========================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🔍 Interactive Filters")
    
    year_range = st.slider("Year Range", int(df["Year"].min()), int(df["Year"].max()), 
                           (int(df["Year"].min()), int(df["Year"].max())), key="year_filter")
    
    risk_levels = st.multiselect("Risk Levels", df["Risk_Level"].unique(), 
                                 default=df["Risk_Level"].unique(), key="risk_filter")
    
    st.markdown("---")
    st.markdown("#### 📊 Gap Analysis")
    gap_threshold = st.slider("Show Gaps Greater Than", int(df["Predicted_Gap"].min()), int(df["Predicted_Gap"].max()), 
                              int(df["Predicted_Gap"].min()), step=50, key="gap_filter")
    
    st.markdown("#### 📦 Order Volume")
    order_min, order_max = st.slider("Order Range", int(df["Orders"].min()), int(df["Orders"].max()),
                                     (int(df["Orders"].min()), int(df["Orders"].max())), key="order_filter")
    
    st.markdown("---")
    st.markdown("#### ⚡ Quick Filters")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 High Risk", use_container_width=True):
            st.session_state.risk_filter = ["High"]
            st.rerun()
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.rerun()

# Apply filters
df_filtered = df[
    (df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1]) &
    (df["Risk_Level"].isin(risk_levels)) & (df["Predicted_Gap"] >= gap_threshold) &
    (df["Orders"] >= order_min) & (df["Orders"] <= order_max)
]

with st.sidebar:
    st.markdown("---")
    st.markdown(f"**Showing {len(df_filtered)} of {len(df)} records**")

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
# METRICS
# =========================
col1, col2, col3, col4 = st.columns(4)

total_gap = df_filtered['Predicted_Gap'].sum()
total_orders = df_filtered['Orders'].sum()
avg_orders = df_filtered['Orders'].mean()
high_risk_count = len(df_filtered[df_filtered['Risk_Level'] == 'High'])

if len(df_filtered) > 0:
    critical_year_row = df_filtered.loc[df_filtered['Risk_Score'].idxmax()]
else:
    critical_year_row = pd.Series({'Year': 'N/A', 'Predicted_Gap': 0})

with col1:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Total Predicted Gap</div>
    <div class='metric-value'>{total_gap:,.0f}</div>
    <div class='metric-delta'>{(total_gap/total_orders*100 if total_orders > 0 else 0):.1f}% of total orders</div></div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>High-Risk Periods</div>
    <div class='metric-value'>{high_risk_count}</div>
    <div class='metric-delta'>{(high_risk_count/len(df_filtered)*100 if len(df_filtered) > 0 else 0):.0f}% of timeline</div></div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Critical Year</div>
    <div class='metric-value'>{critical_year_row['Year']}</div>
    <div class='metric-delta'>Gap: {critical_year_row['Predicted_Gap']:,} units</div></div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""<div class='metric-card'><div class='metric-label'>Total Orders</div>
    <div class='metric-value'>{total_orders:,}</div>
    <div class='metric-delta'>Average: {avg_orders:.0f} per year</div></div>""", unsafe_allow_html=True)

# =========================
# ALERT
# =========================
high_risk_years = df_filtered[df_filtered['Risk_Level'] == 'High']['Year'].tolist()
if high_risk_years:
    st.markdown(f"""<div class='alert-box critical'><h4>⚠️ CRITICAL ALERT: High-Risk Periods Detected</h4>
    <p style='margin: 0; font-size: 1rem; line-height: 1.6;'><strong>Affected Years:</strong> {', '.join(map(str, high_risk_years))}<br>
    <strong>Action Required:</strong> Immediate supplier oversight and capacity planning review needed.</p></div>""", unsafe_allow_html=True)

# =========================
# INTERACTIVE TABS
# =========================
st.markdown("<h2 class='section-header'>ANALYSIS VIEWS</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📈 Production Trends", "🎯 Correlation Analysis", "📊 Risk Breakdown", "🗓️ Year-by-Year"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        chart_type = st.radio("Chart Type:", ["Line Chart", "Area Chart", "Bar Chart"], horizontal=True)
        
        fig1 = go.Figure()
        
        if chart_type == "Line Chart":
            fig1.add_trace(go.Scatter(x=df_filtered['Year'], y=df_filtered['ProductionGap'], name='Actual Gap',
                                     mode='lines+markers', line=dict(color='#5B6B7C', width=3), marker=dict(size=8)))
            fig1.add_trace(go.Scatter(x=df_filtered['Year'], y=df_filtered['Predicted_Gap'], name='Predicted Gap',
                                     mode='lines+markers', line=dict(color='#0039A6', width=4), marker=dict(size=10, symbol='diamond')))
        elif chart_type == "Area Chart":
            fig1.add_trace(go.Scatter(x=df_filtered['Year'], y=df_filtered['ProductionGap'], name='Actual Gap',
                                     fill='tozeroy', fillcolor='rgba(91, 107, 124, 0.3)', line=dict(color='#5B6B7C')))
            fig1.add_trace(go.Scatter(x=df_filtered['Year'], y=df_filtered['Predicted_Gap'], name='Predicted Gap',
                                     fill='tozeroy', fillcolor='rgba(0, 57, 166, 0.3)', line=dict(color='#0039A6')))
        else:
            fig1.add_trace(go.Bar(x=df_filtered['Year'], y=df_filtered['ProductionGap'], name='Actual Gap', marker_color='#5B6B7C'))
            fig1.add_trace(go.Bar(x=df_filtered['Year'], y=df_filtered['Predicted_Gap'], name='Predicted Gap', marker_color='#0039A6'))
        
        fig1.update_layout(title='Production Gap: Actual vs Predicted', xaxis_title='Year', yaxis_title='Gap (Units)',
                          template='plotly_white', height=450, hovermode='x unified',
                          legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("#### Risk Level Distribution")
        risk_counts = df_filtered['Risk_Level'].value_counts()
        
        for level in ['High', 'Medium', 'Low']:
            if level in risk_counts.index:
                count = risk_counts[level]
                perc = (count / len(df_filtered)) * 100
                color = {'High': '#C81E1E', 'Medium': '#F57C00', 'Low': '#0B8043'}[level]
                st.markdown(f"""<div class='risk-item'><div class='risk-header'>
                <span class='risk-label'>{level} Risk</span><span class='risk-count' style='color:{color}'>{count} ({perc:.0f}%)</span></div>
                <div class='risk-bar-bg'><div class='risk-bar-fill' style='width:{perc}%; background:{color};'></div></div></div>""", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        scatter_color = st.selectbox("Color by:", ["Risk Level", "Year"])
    with col2:
        scatter_size = st.selectbox("Size by:", ["Risk Score", "Orders", "Predicted Gap"])
    
    color_col = df_filtered['Risk_Score'] if scatter_color == "Risk Level" else df_filtered['Year']
    colorscale = [[0, '#0B8043'], [0.5, '#F57C00'], [1, '#C81E1E']] if scatter_color == "Risk Level" else [[0, '#001F5B'], [0.5, '#0039A6'], [1, '#005EB8']]
    size_col = df_filtered['Risk_Score']*12 if scatter_size == "Risk Score" else df_filtered['Orders']/10 if scatter_size == "Orders" else df_filtered['Predicted_Gap']/10
    
    fig_scatter = go.Figure(data=go.Scatter(x=df_filtered['Orders'], y=df_filtered['Predicted_Gap'], mode='markers',
                                           marker=dict(size=size_col, color=color_col, colorscale=colorscale, showscale=True, colorbar=dict(title=scatter_color)),
                                           text=df_filtered['Year'], hovertemplate='<b>Year %{text}</b><br>Orders: %{x:,}<br>Gap: %{y:,}<extra></extra>'))
    fig_scatter.update_layout(title='Orders vs Predicted Gap Analysis', xaxis_title='Orders', yaxis_title='Predicted Gap',
                             template='plotly_white', height=500, hovermode='closest')
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Risk Distribution by Count")
        risk_counts = df_filtered['Risk_Level'].value_counts()
        fig_pie = go.Figure(data=[go.Pie(labels=risk_counts.index, values=risk_counts.values,
                                        marker=dict(colors=['#C81E1E', '#F57C00', '#0B8043']), hole=0.4,
                                        textinfo='label+percent', textfont=dict(size=14))])
        fig_pie.update_layout(height=400, showlegend=True, template='plotly_white')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("#### Gap by Risk Level")
        gap_by_risk = df_filtered.groupby('Risk_Level')['Predicted_Gap'].sum().reset_index()
        fig_bar = go.Figure(data=[go.Bar(x=gap_by_risk['Risk_Level'], y=gap_by_risk['Predicted_Gap'],
                                        marker_color=['#0B8043', '#F57C00', '#C81E1E'],
                                        text=gap_by_risk['Predicted_Gap'], texttemplate='%{text:,.0f}', textposition='outside')])
        fig_bar.update_layout(height=400, xaxis_title='Risk Level', yaxis_title='Total Predicted Gap',
                            template='plotly_white', showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    selected_year = st.selectbox("Select Year for Detailed View:", df_filtered['Year'].unique())
    year_data = df_filtered[df_filtered['Year'] == selected_year].iloc[0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Orders", f"{year_data['Orders']:,}")
        st.metric("Production Gap", f"{year_data['ProductionGap']:,}")
    with col2:
        st.metric("Predicted Gap", f"{year_data['Predicted_Gap']:,}")
        st.metric("Risk Level", year_data['Risk_Level'])
    with col3:
        variance = year_data['Predicted_Gap'] - year_data['ProductionGap']
        st.metric("Prediction Variance", f"{variance:,.0f}", f"{(variance/year_data['ProductionGap']*100 if year_data['ProductionGap'] != 0 else 0):.1f}%")
    
    st.markdown("#### Historical Comparison")
    fig_compare = make_subplots(specs=[[{"secondary_y": True}]])
    fig_compare.add_trace(go.Bar(x=df_filtered['Year'], y=df_filtered['Orders'], name='Orders', marker_color='#0039A6'), secondary_y=False)
    fig_compare.add_trace(go.Scatter(x=df_filtered['Year'], y=df_filtered['Predicted_Gap'], name='Predicted Gap',
                                    mode='lines+markers', marker=dict(size=10, color='#C81E1E'), line=dict(width=3, color='#C81E1E')), secondary_y=True)
    fig_compare.update_yaxes(title_text="Orders", secondary_y=False)
    fig_compare.update_yaxes(title_text="Predicted Gap", secondary_y=True)
    fig_compare.update_layout(height=400, template='plotly_white', hovermode='x unified',
                             legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_compare, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ROADMAP
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

selected_phase = st.selectbox("Select Phase for Details:", phases['Phase'].tolist())
phase_info = phases[phases['Phase'] == selected_phase].iloc[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Progress", f"{phase_info['Progress']}%")
with col2:
    st.metric("Start Date", phase_info['Start'].strftime('%Y-%m-%d'))
with col3:
    st.metric("End Date", phase_info['Finish'].strftime('%Y-%m-%d'))

colors = {'Planning': '#001F5B', 'Implementation': '#0039A6', 'Integration': '#005EB8',
          'Analytics': '#1976D2', 'Deployment': '#42A5F5', 'Review': '#90CAF9'}

fig3 = px.timeline(phases, x_start="Start", x_end="Finish", y="Phase", color="Category", color_discrete_map=colors)
fig3.update_yaxes(autorange="reversed")
fig3.update_layout(height=400, title='Project Timeline', template='plotly_white', xaxis_title="Timeline", yaxis_title="")
st.plotly_chart(fig3, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

cols = st.columns(6)
for col, row in zip(cols, phases.itertuples()):
    with col:
        st.markdown(f"<div class='phase-card'><div class='phase-progress'>{row.Progress}%</div><div class='phase-label'>{row.Category}</div></div>", unsafe_allow_html=True)

# =========================
# RECOMMENDATIONS
# =========================
st.markdown("<h2 class='section-header'>STRATEGIC RECOMMENDATIONS</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""<div class='alert-box critical'><h4>🚨 Critical Actions Required</h4><ul>
    <li>Implement real-time telemetry systems for all high-risk tier-1 suppliers</li>
    <li>Establish automated alert protocols for KPI deviation thresholds</li>
    <li>Increase oversight frequency and audit schedules for 2026-2027 period</li>
    <li>Deploy contingency supplier identification and qualification process</li></ul></div>""", unsafe_allow_html=True)
    
    st.markdown("""<div class='alert-box success'><h4>✅ Quick Win Initiatives</h4><ul>
    <li>Deploy executive dashboard for real-time leadership visibility</li>
    <li>Integrate supplier portals with central monitoring infrastructure</li>
    <li>Automate weekly risk assessment and distribution reports</li>
    <li>Establish cross-functional risk review committee</li></ul></div>""", unsafe_allow_html=True)

with col2:
    st.markdown("""<div class='alert-box info'><h4>📋 Long-Term Strategic Initiatives</h4><ul>
    <li>Develop ML-powered predictive capacity planning models</li>
    <li>Expand digital oversight framework to tier-2 and tier-3 suppliers</li>
    <li>Create comprehensive supplier performance scorecard system</li>
    <li>Invest in AI-powered anomaly detection and early warning systems</li>
    <li>Build supplier resilience index and diversification metrics</li></ul></div>""", unsafe_allow_html=True)

# =========================
# DATA TABLE
# =========================
st.markdown("<h2 class='section-header'>DETAILED DATA TABLE</h2>", unsafe_allow_html=True)

with st.expander("📊 View Complete Dataset", expanded=False):
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.dataframe(df_filtered.style.background_gradient(subset=['Risk_Score'], cmap='RdYlGn_r'), use_container_width=True, height=400)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("""
<div class='dashboard-footer'>
    <p class='footer-title'>BOEING DIGITAL OVERSIGHT SYSTEM | VERSION 2.0</p>
    <p class='footer-meta'>© 2025 The Boeing Company | Powered by Advanced Analytics & Machine Learning<br>
    Last Updated: November 2025 | Confidential & Proprietary</p>
</div>
""", unsafe_allow_html=True)
