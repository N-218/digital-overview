import streamlit as st 

import pandas as pd 

import plotly.express as px 

import plotly.graph_objects as go 

from plotly.subplots import make_subplots 

 

# ========================= 

# PAGE CONFIGURATION 

# ========================= 

st.set_page_config( 

    page_title="Boeing Digital Oversight Dashboard", 

    layout="wide", 

    page_icon="✈️", 

    initial_sidebar_state="expanded" 

) 

 

# ========================= 

# BOEING BRAND COLORS & CUSTOM STYLE 

# ========================= 

st.markdown(""" 

<style> 

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'); 

 

.stApp { 

    background: #f8fafc; 

    font-family: 'Inter', 'Segoe UI', sans-serif; 

} 

 

/* Header Styling */ 

.dashboard-header { 

    background: linear-gradient(135deg, #003087 0%, #0052CC 100%); 

    padding: 2.5rem 2rem; 

    border-radius: 12px; 

    margin-bottom: 2rem; 

    box-shadow: 0 4px 20px rgba(0, 48, 135, 0.15); 

} 

 

.dashboard-title { 

    color: white; 

    font-size: 2.5rem; 

    font-weight: 700; 

    margin: 0; 

    letter-spacing: -0.5px; 

} 

 

.dashboard-subtitle { 

    color: #a8c5e8; 

    font-size: 1.1rem; 

    margin-top: 0.5rem; 

    font-weight: 400; 

} 

 

/* Metric Cards */ 

.metric-card { 

    background: white; 

    padding: 1.5rem; 

    border-radius: 10px; 

    box-shadow: 0 2px 8px rgba(0,0,0,0.08); 

    border-left: 4px solid #003087; 

    transition: transform 0.2s, box-shadow 0.2s; 

} 

 

.metric-card:hover { 

    transform: translateY(-2px); 

    box-shadow: 0 4px 16px rgba(0,0,0,0.12); 

} 

 

.metric-label { 

    color: #64748b; 

    font-size: 0.875rem; 

    font-weight: 500; 

    text-transform: uppercase; 

    letter-spacing: 0.5px; 

    margin-bottom: 0.5rem; 

} 

 

.metric-value { 

    color: #003087; 

    font-size: 2rem; 

    font-weight: 700; 

    line-height: 1; 

} 

 

.metric-delta { 

    color: #10b981; 

    font-size: 0.875rem; 

    margin-top: 0.5rem; 

} 

 

/* Sidebar Styling */ 

.css-1d391kg, [data-testid="stSidebar"] { 

    background: linear-gradient(180deg, #003087 0%, #0052CC 100%); 

} 

 

.css-1d391kg .sidebar-content { 

    color: white; 

} 

 

/* Section Headers */ 

.section-header { 

    color: #003087; 

    font-size: 1.5rem; 

    font-weight: 600; 

    margin: 2rem 0 1rem 0; 

    padding-bottom: 0.5rem; 

    border-bottom: 2px solid #e2e8f0; 

} 

 

/* Alert Box */ 

.alert-box { 

    background: #fef3c7; 

    border-left: 4px solid #f59e0b; 

    padding: 1rem 1.5rem; 

    border-radius: 8px; 

    margin: 1rem 0; 

} 

 

.alert-box.critical { 

    background: #fee2e2; 

    border-left-color: #dc2626; 

} 

 

.alert-box.success { 

    background: #d1fae5; 

    border-left-color: #10b981; 

} 

 

/* Status Badge */ 

.status-badge { 

    display: inline-block; 

    padding: 0.25rem 0.75rem; 

    border-radius: 20px; 

    font-size: 0.75rem; 

    font-weight: 600; 

    text-transform: uppercase; 

    letter-spacing: 0.5px; 

} 

 

.status-high { 

    background: #fee2e2; 

    color: #991b1b; 

} 

 

.status-medium { 

    background: #fef3c7; 

    color: #92400e; 

} 

 

.status-low { 

    background: #d1fae5; 

    color: #065f46; 

} 

 

/* Chart Container */ 

.chart-container { 

    background: white; 

    padding: 1.5rem; 

    border-radius: 10px; 

    box-shadow: 0 2px 8px rgba(0,0,0,0.08); 

    margin-bottom: 1.5rem; 

} 

 

/* Boeing Logo Space */ 

.logo-space { 

    text-align: right; 

    color: white; 

    font-weight: 600; 

    font-size: 1.5rem; 

    letter-spacing: 2px; 

} 

 

h1, h2, h3 { 

    color: #003087; 

} 

 

[data-testid="stMetricValue"] { 

    color: #003087 !important; 

    font-size: 1.75rem !important; 

    font-weight: 700 !important; 

} 

 

[data-testid="stMetricLabel"] { 

    color: #64748b !important; 

    font-size: 0.875rem !important; 

    font-weight: 500 !important; 

} 

 

.stButton>button { 

    background: #003087; 

    color: white; 

    border: none; 

    border-radius: 6px; 

    padding: 0.5rem 1.5rem; 

    font-weight: 600; 

    transition: all 0.2s; 

} 

 

.stButton>button:hover { 

    background: #0052CC; 

    box-shadow: 0 4px 12px rgba(0,48,135,0.3); 

} 

 

/* Sidebar Styling */ 

[data-testid="stSidebar"] { 

    background: #1e293b; 

} 

 

[data-testid="stSidebar"] .stMarkdown { 

    color: white; 

} 

 

</style> 

""", unsafe_allow_html=True) 

 

# ========================= 

# SIDEBAR (Upload & Filters) 

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

 

# Load Data 

df = pd.read_csv(uploaded_file) 

 

# Convert Risk Level to Numeric Score 

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

     

    risk_levels = st.multiselect( 

        "Risk Levels", 

        df["Risk_Level"].unique(), 

        default=df["Risk_Level"].unique() 

    ) 

     

    st.markdown("---") 

    st.markdown("### 📊 Quick Stats") 

    st.metric("Total Years", len(df_filtered := df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1]) & df["Risk_Level"].isin(risk_levels)])) 

    st.metric("Avg Gap", f"{df_filtered['Predicted_Gap'].mean():.1f}") 

 

# Apply Filters 

df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])] 

df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)] 

 

# ========================= 

# HEADER 

# ========================= 

st.markdown(""" 

<div class='dashboard-header'> 

    <div style='display: flex; justify-content: space-between; align-items: center;'> 

        <div> 

            <h1 class='dashboard-title'>Digital Oversight Dashboard</h1> 

            <p class='dashboard-subtitle'>Supply Chain Intelligence & Risk Management System</p> 

        </div> 

        <div class='logo-space'> 

            ✈️ 

        </div> 

    </div> 

</div> 

""", unsafe_allow_html=True) 

 

# ========================= 

# KEY METRICS WITH ENHANCED CARDS 

# ========================= 

col1, col2, col3, col4 = st.columns(4) 

 

with col1: 

    total_gap = df_filtered['Predicted_Gap'].sum() 

    st.metric( 

        "Total Predicted Gap", 

        f"{total_gap:,.0f}", 

        delta=f"{((total_gap / df_filtered['Orders'].sum()) * 100):.1f}% of orders", 

        delta_color="inverse" 

    ) 

 

with col2: 

    high_risk_count = len(df_filtered[df_filtered['Risk_Level'] == 'High']) 

    st.metric( 

        "High-Risk Periods", 

        high_risk_count, 

        delta=f"{(high_risk_count/len(df_filtered)*100):.0f}% of timeline" 

    ) 

 

with col3: 

    critical_year = df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year'] 

    critical_gap = df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Predicted_Gap'] 

    st.metric( 

        "Critical Year", 

        f"{critical_year}", 

        delta=f"Gap: {critical_gap:,.0f}", 

        delta_color="inverse" 

    ) 

 

with col4: 

    total_orders = df_filtered['Orders'].sum() 

    avg_orders = df_filtered['Orders'].mean() 

    st.metric( 

        "Total Orders", 

        f"{total_orders:,.0f}", 

        delta=f"Avg: {avg_orders:,.0f}/yr" 

    ) 

 

# Risk Alert Banner 

high_risk_years = df_filtered[df_filtered['Risk_Level'] == 'High']['Year'].tolist() 

if high_risk_years: 

    st.markdown(f""" 

    <div class='alert-box critical'> 

        <strong>⚠️ Critical Alert:</strong> High-risk periods detected in years: <strong>{', '.join(map(str, high_risk_years))}</strong> 

        <br>Immediate action required for supplier oversight and capacity planning. 

    </div> 

    """, unsafe_allow_html=True) 

 

# ========================= 

# MAIN VISUALIZATIONS 

# ========================= 

st.markdown("<h2 class='section-header'>📈 Production Analysis & Forecasting</h2>", unsafe_allow_html=True) 

 

col1, col2 = st.columns([3, 2]) 

 

with col1: 

    # Enhanced Production Gap Chart 

    fig1 = go.Figure() 

     

    fig1.add_trace(go.Scatter( 

        x=df_filtered['Year'], 

        y=df_filtered['ProductionGap'], 

        name='Actual Gap', 

        mode='lines+markers', 

        line=dict(color='#94a3b8', width=3), 

        marker=dict(size=8, color='#94a3b8') 

    )) 

     

    fig1.add_trace(go.Scatter( 

        x=df_filtered['Year'], 

        y=df_filtered['Predicted_Gap'], 

        name='Predicted Gap', 

        mode='lines+markers', 

        line=dict(color='#003087', width=4), 

        marker=dict(size=10, color='#003087', symbol='diamond') 

    )) 

     

    fig1.update_layout( 

        title={ 

            'text': 'Production Gap: Actual vs Predicted (2021-2028)', 

            'x': 0.5, 

            'xanchor': 'center', 

            'font': {'size': 18, 'color': '#003087', 'family': 'Inter'} 

        }, 

        xaxis_title='Year', 

        yaxis_title='Gap (Units)', 

        template='plotly_white', 

        height=450, 

        hovermode='x unified', 

        legend=dict( 

            orientation="h", 

            yanchor="bottom", 

            y=1.02, 

            xanchor="right", 

            x=1 

        ), 

        plot_bgcolor='rgba(0,0,0,0)', 

        paper_bgcolor='rgba(0,0,0,0)' 

    ) 

     

    fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

    fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

     

    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False}) 

 

with col2: 

    # Risk Distribution Gauge 

    risk_counts = df_filtered['Risk_Level'].value_counts() 

     

    fig_gauge = go.Figure(go.Indicator( 

        mode="gauge+number+delta", 

        value=df_filtered['Risk_Score'].mean(), 

        title={'text': "Average Risk Level", 'font': {'size': 16, 'color': '#003087'}}, 

        delta={'reference': 2, 'increasing': {'color': "#dc2626"}}, 

        gauge={ 

            'axis': {'range': [None, 3], 'tickwidth': 1, 'tickcolor': "#003087"}, 

            'bar': {'color': "#003087"}, 

            'bgcolor': "white", 

            'borderwidth': 2, 

            'bordercolor': "#e2e8f0", 

            'steps': [ 

                {'range': [0, 1], 'color': '#d1fae5'}, 

                {'range': [1, 2], 'color': '#fef3c7'}, 

                {'range': [2, 3], 'color': '#fee2e2'} 

            ], 

            'threshold': { 

                'line': {'color': "red", 'width': 4}, 

                'thickness': 0.75, 

                'value': 2.5 

            } 

        } 

    )) 

     

    fig_gauge.update_layout( 

        height=250, 

        margin=dict(l=20, r=20, t=50, b=20), 

        paper_bgcolor='rgba(0,0,0,0)', 

        font={'family': 'Inter'} 

    ) 

     

    st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False}) 

     

    # Risk Distribution 

    st.markdown("#### Risk Distribution") 

    for level in ['High', 'Medium', 'Low']: 

        if level in risk_counts.index: 

            count = risk_counts[level] 

            percentage = (count / len(df_filtered)) * 100 

            color = {'High': '#dc2626', 'Medium': '#f59e0b', 'Low': '#10b981'}[level] 

            st.markdown(f""" 

            <div style='margin: 0.5rem 0;'> 

                <div style='display: flex; justify-content: space-between; margin-bottom: 0.25rem;'> 

                    <span style='font-weight: 600; color: #64748b;'>{level}</span> 

                    <span style='color: {color}; font-weight: 600;'>{count} ({percentage:.0f}%)</span> 

                </div> 

                <div style='background: #e2e8f0; border-radius: 10px; height: 8px; overflow: hidden;'> 

                    <div style='background: {color}; width: {percentage}%; height: 100%;'></div> 

                </div> 

            </div> 

            """, unsafe_allow_html=True) 

 

# ========================= 

# ORDERS vs GAP ANALYSIS 

# ========================= 

st.markdown("<h2 class='section-header'>🎯 Orders & Gap Correlation</h2>", unsafe_allow_html=True) 

 

fig2 = make_subplots( 

    rows=1, cols=2, 

    subplot_titles=('Orders vs Predicted Gap', 'Year-over-Year Risk Progression'), 

    specs=[[{"secondary_y": False}, {"type": "bar"}]] 

) 

 

# Scatter plot 

fig2.add_trace( 

    go.Scatter( 

        x=df_filtered['Orders'], 

        y=df_filtered['Predicted_Gap'], 

        mode='markers', 

        marker=dict( 

            size=df_filtered['Risk_Score']*10, 

            color=df_filtered['Risk_Score'], 

            colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#dc2626']], 

            showscale=True, 

            colorbar=dict(title="Risk", x=0.45) 

        ), 

        text=df_filtered['Year'], 

        hovertemplate='<b>Year %{text}</b><br>Orders: %{x}<br>Gap: %{y}<extra></extra>', 

        name='Year Data' 

    ), 

    row=1, col=1 

) 

 

# Risk bar chart 

colors_map = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#dc2626'} 

fig2.add_trace( 

    go.Bar( 

        x=df_filtered['Year'], 

        y=df_filtered['Risk_Score'], 

        marker_color=[colors_map[level] for level in df_filtered['Risk_Level']], 

        text=df_filtered['Risk_Level'], 

        textposition='outside', 

        name='Risk Level', 

        hovertemplate='<b>%{x}</b><br>Risk: %{text}<extra></extra>' 

    ), 

    row=1, col=2 

) 

 

fig2.update_xaxes(title_text="Orders", row=1, col=1, showgrid=True, gridcolor='#e2e8f0') 

fig2.update_yaxes(title_text="Predicted Gap", row=1, col=1, showgrid=True, gridcolor='#e2e8f0') 

fig2.update_xaxes(title_text="Year", row=1, col=2, showgrid=False) 

fig2.update_yaxes(title_text="Risk Score", row=1, col=2, showgrid=True, gridcolor='#e2e8f0') 

 

fig2.update_layout( 

    height=400, 

    showlegend=False, 

    template='plotly_white', 

    paper_bgcolor='rgba(0,0,0,0)', 

    plot_bgcolor='rgba(0,0,0,0)', 

    font={'family': 'Inter'} 

) 

 

st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False}) 

 

# ========================= 

# IMPLEMENTATION ROADMAP 

# ========================= 

st.markdown("<h2 class='section-header'>🗺️ Implementation Roadmap 2025</h2>", unsafe_allow_html=True) 

 

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

    'Planning': '#003087', 

    'Implementation': '#0052CC', 

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

    color_discrete_map=colors, 

    title="Project Timeline & Progress" 

) 

 

fig3.update_yaxes(autorange="reversed") 

fig3.update_layout( 

    height=400, 

    title={ 

        'x': 0.5, 

        'xanchor': 'center', 

        'font': {'size': 18, 'color': '#003087', 'family': 'Inter'} 

    }, 

    template='plotly_white', 

    paper_bgcolor='rgba(0,0,0,0)', 

    plot_bgcolor='rgba(0,0,0,0)', 

    xaxis_title='Timeline', 

    yaxis_title='', 

    font={'family': 'Inter'} 

) 

 

st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False}) 

 

# Progress indicators 

col1, col2, col3, col4, col5, col6 = st.columns(6) 

for idx, (col, row) in enumerate(zip([col1, col2, col3, col4, col5, col6], phases.itertuples())): 

    with col: 

        st.markdown(f""" 

        <div style='text-align: center; padding: 1rem; background: white; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);'> 

            <div style='font-size: 1.5rem; font-weight: 700; color: #003087;'>{row.Progress}%</div> 

            <div style='font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;'>{row.Category}</div> 

        </div> 

        """, unsafe_allow_html=True) 

 

# ========================= 

# STRATEGIC RECOMMENDATIONS 

# ========================= 

st.markdown("<h2 class='section-header'>💡 Strategic Recommendations</h2>", unsafe_allow_html=True) 

 

col1, col2 = st.columns(2) 

 

with col1: 

    st.markdown(""" 

    <div class='alert-box critical'> 

        <h4 style='margin-top: 0; color: #991b1b;'>🚨 Critical Actions</h4> 

        <ul style='margin-bottom: 0;'> 

            <li>Implement real-time telemetry for high-risk suppliers</li> 

            <li>Establish automated alert system for KPI deviations</li> 

            <li>Increase oversight frequency during 2026-2027 period</li> 

        </ul> 

    </div> 

    """, unsafe_allow_html=True) 

     

    st.markdown(""" 

    <div class='alert-box success'> 

        <h4 style='margin-top: 0; color: #065f46;'>✅ Quick Wins</h4> 

        <ul style='margin-bottom: 0;'> 

            <li>Deploy dashboard for leadership visibility</li> 

            <li>Integrate supplier portals with central monitoring</li> 

            <li>Automate weekly risk reports</li> 

        </ul> 

    </div> 

    """, unsafe_allow_html=True) 

 

with col2: 

    st.markdown(""" 

    <div class='alert-box'> 

        <h4 style='margin-top: 0; color: #92400e;'>📋 Long-term Strategy</h4> 

        <ul style='margin-bottom: 0;'> 

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

    st.dataframe( 

        df_filtered.style.background_gradient(subset=['Risk_Score'], cmap='RdYlGn_r'), 

        use_container_width=True, 

        height=400 

    ) 

 

# ========================= 

# FOOTER 

# ========================= 

st.markdown("<br><br>", unsafe_allow_html=True) 

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
