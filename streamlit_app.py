import streamlit as st 

import pandas as pd 

import plotly.express as px 

import plotly.graph_objects as go 

from plotly.subplots import make_subplots 

import numpy as np 

 

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

        st.info("👆 Upload your CSV file to begin") 

        st.stop() 

 

# Load Data 

df = pd.read_csv(uploaded_file) 

 

# Clean column names (remove any extra spaces) 

df.columns = df.columns.str.strip() 

 

# Convert Risk Level to Numeric Score 

risk_mapping = {"Low": 1, "Medium": 2, "High": 3} 

df["Risk_Score"] = df["Risk_Level"].map(risk_mapping) 

 

# Fill NaN values with 0 for numeric columns 

numeric_cols = ['PlannedOutput', 'ActualOutput', 'Orders', 'Backlog', 'ProductionGap',  

                'Predicted_Gap', 'NetLoss', 'ForwardLosses', 'ExcessCapacityCost'] 

for col in numeric_cols: 

    if col in df.columns: 

        df[col] = df[col].fillna(0) 

 

# Sidebar Filters 

with st.sidebar: 

    st.markdown("### 🔍 Filters") 

     

    year_range = st.slider( 

        "Year Range", 

        int(df["Year"].min()), 

        int(df["Year"].max()), 

        (int(df["Year"].min()), int(df["Year"].max())) 

    ) 

     

    available_risks = df["Risk_Level"].dropna().unique().tolist() 

    risk_levels = st.multiselect( 

        "Risk Levels", 

        available_risks, 

        default=available_risks 

    ) 

     

    st.markdown("---") 

    st.markdown("### 📊 Dashboard Info") 

    st.info("Displaying production, backlog, and risk metrics for Boeing supply chain oversight") 

 

# Apply Filters 

df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])] 

if risk_levels: 

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

        <div style='text-align: right; color: white; font-weight: 600; font-size: 1.5rem; letter-spacing: 2px;'> 

            ✈️ 

        </div> 

    </div> 

</div> 

""", unsafe_allow_html=True) 

 

# ========================= 

# KEY METRICS 

# ========================= 

col1, col2, col3, col4, col5 = st.columns(5) 

 

with col1: 

    total_orders = df_filtered['Orders'].sum() 

    st.metric( 

        "Total Orders", 

        f"{total_orders:,.0f}", 

        delta=None 

    ) 

 

with col2: 

    total_backlog = df_filtered['Backlog'].sum() 

    st.metric( 

        "Total Backlog", 

        f"{total_backlog:,.0f}", 

        delta=None 

    ) 

 

with col3: 

    total_gap = df_filtered['ProductionGap'].sum() 

    st.metric( 

        "Production Gap", 

        f"{total_gap:,.0f}", 

        delta="Actual", 

        delta_color="inverse" 

    ) 

 

with col4: 

    predicted_gap = df_filtered['Predicted_Gap'].sum() 

    st.metric( 

        "Predicted Gap", 

        f"{predicted_gap:,.1f}", 

        delta="Forecast", 

        delta_color="inverse" 

    ) 

 

with col5: 

    high_risk_count = len(df_filtered[df_filtered['Risk_Level'] == 'High']) 

    st.metric( 

        "High-Risk Years", 

        high_risk_count, 

        delta=f"{(high_risk_count/len(df_filtered)*100) if len(df_filtered) > 0 else 0:.0f}%" 

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

# PRODUCTION ANALYSIS 

# ========================= 

st.markdown("<h2 class='section-header'>📈 Production & Output Analysis</h2>", unsafe_allow_html=True) 

 

col1, col2 = st.columns(2) 

 

with col1: 

    # Production vs Orders Chart 

    fig1 = go.Figure() 

     

    # Filter data for years with actual values 

    df_actual = df_filtered[df_filtered['PlannedOutput'] > 0] 

     

    fig1.add_trace(go.Bar( 

        x=df_actual['Year'], 

        y=df_actual['PlannedOutput'], 

        name='Planned Output', 

        marker_color='#60a5fa', 

        opacity=0.7 

    )) 

     

    fig1.add_trace(go.Bar( 

        x=df_actual['Year'], 

        y=df_actual['ActualOutput'], 

        name='Actual Output', 

        marker_color='#003087' 

    )) 

     

    fig1.add_trace(go.Scatter( 

        x=df_actual['Year'], 

        y=df_actual['Orders'], 

        name='Orders', 

        mode='lines+markers', 

        line=dict(color='#dc2626', width=3), 

        marker=dict(size=10, symbol='diamond') 

    )) 

     

    fig1.update_layout( 

        title={ 

            'text': 'Production Output vs Orders', 

            'x': 0.5, 

            'xanchor': 'center', 

            'font': {'size': 18, 'color': '#003087', 'family': 'Inter'} 

        }, 

        xaxis_title='Year', 

        yaxis_title='Units', 

        template='plotly_white', 

        height=450, 

        hovermode='x unified', 

        barmode='group', 

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

    # Backlog Trend 

    fig2 = go.Figure() 

     

    df_backlog = df_filtered[df_filtered['Backlog'] > 0] 

     

    fig2.add_trace(go.Scatter( 

        x=df_backlog['Year'], 

        y=df_backlog['Backlog'], 

        mode='lines+markers', 

        name='Backlog', 

        line=dict(color='#003087', width=4), 

        marker=dict(size=12, color='#003087'), 

        fill='tozeroy', 

        fillcolor='rgba(0, 48, 135, 0.1)' 

    )) 

     

    fig2.update_layout( 

        title={ 

            'text': 'Backlog Trend Over Time', 

            'x': 0.5, 

            'xanchor': 'center', 

            'font': {'size': 18, 'color': '#003087', 'family': 'Inter'} 

        }, 

        xaxis_title='Year', 

        yaxis_title='Backlog (Units)', 

        template='plotly_white', 

        height=450, 

        hovermode='x unified', 

        plot_bgcolor='rgba(0,0,0,0)', 

        paper_bgcolor='rgba(0,0,0,0)' 

    ) 

     

    fig2.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

    fig2.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

     

    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False}) 

 

# ========================= 

# GAP ANALYSIS 

# ========================= 

st.markdown("<h2 class='section-header'>🎯 Production Gap Analysis</h2>", unsafe_allow_html=True) 

 

col1, col2 = st.columns([3, 2]) 

 

with col1: 

    # Gap Comparison 

    fig3 = go.Figure() 

     

    fig3.add_trace(go.Bar( 

        x=df_filtered['Year'], 

        y=df_filtered['ProductionGap'], 

        name='Actual Gap', 

        marker_color='#94a3b8', 

        opacity=0.7 

    )) 

     

    fig3.add_trace(go.Scatter( 

        x=df_filtered['Year'], 

        y=df_filtered['Predicted_Gap'], 

        name='Predicted Gap', 

        mode='lines+markers', 

        line=dict(color='#dc2626', width=4), 

        marker=dict(size=10, color='#dc2626', symbol='diamond') 

    )) 

     

    fig3.update_layout( 

        title={ 

            'text': 'Production Gap: Actual vs Predicted', 

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

     

    fig3.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

    fig3.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

     

    st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False}) 

 

with col2: 

    # Risk Level by Year 

    colors_map = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#dc2626'} 

     

    fig4 = go.Figure() 

     

    for risk_level in ['Low', 'Medium', 'High']: 

        df_risk = df_filtered[df_filtered['Risk_Level'] == risk_level] 

        if not df_risk.empty: 

            fig4.add_trace(go.Bar( 

                x=df_risk['Year'], 

                y=df_risk['Risk_Score'], 

                name=risk_level, 

                marker_color=colors_map[risk_level], 

                text=risk_level, 

                textposition='inside' 

            )) 

     

    fig4.update_layout( 

        title={ 

            'text': 'Risk Assessment by Year', 

            'x': 0.5, 

            'xanchor': 'center', 

            'font': {'size': 18, 'color': '#003087', 'family': 'Inter'} 

        }, 

        xaxis_title='Year', 

        yaxis_title='Risk Score', 

        template='plotly_white', 

        height=450, 

        barmode='stack', 

        showlegend=True, 

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

     

    fig4.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

    fig4.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

     

    st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False}) 

 

# ========================= 

# FINANCIAL IMPACT 

# ========================= 

st.markdown("<h2 class='section-header'>💰 Financial Impact Analysis</h2>", unsafe_allow_html=True) 

 

# Filter for rows with financial data 

df_financial = df_filtered[(df_filtered['NetLoss'] != 0) | (df_filtered['ForwardLosses'] != 0) | (df_filtered['ExcessCapacityCost'] != 0)] 

 

if not df_financial.empty: 

    fig5 = go.Figure() 

     

    fig5.add_trace(go.Bar( 

        x=df_financial['Year'], 

        y=df_financial['NetLoss'], 

        name='Net Loss', 

        marker_color='#dc2626' 

    )) 

     

    fig5.add_trace(go.Bar( 

        x=df_financial['Year'], 

        y=df_financial['ForwardLosses'], 

        name='Forward Losses', 

        marker_color='#f59e0b' 

    )) 

     

    fig5.add_trace(go.Bar( 

        x=df_financial['Year'], 

        y=df_financial['ExcessCapacityCost'], 

        name='Excess Capacity Cost', 

        marker_color='#3b82f6' 

    )) 

     

    fig5.update_layout( 

        title={ 

            'text': 'Financial Losses & Costs Breakdown', 

            'x': 0.5, 

            'xanchor': 'center', 

            'font': {'size': 18, 'color': '#003087', 'family': 'Inter'} 

        }, 

        xaxis_title='Year', 

        yaxis_title='Amount ($M)', 

        template='plotly_white', 

        height=400, 

        barmode='group', 

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

     

    fig5.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

    fig5.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0') 

     

    st.plotly_chart(fig5, use_container_width=True, config={'displayModeBar': False}) 

else: 

    st.info("No financial impact data available for selected period") 

 

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

 

fig6 = px.timeline( 

    phases, 

    x_start="Start", 

    x_end="Finish", 

    y="Phase", 

    color="Category", 

    color_discrete_map=colors, 

    title="Project Timeline & Progress" 

) 

 

fig6.update_yaxes(autorange="reversed") 

fig6.update_layout( 

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

 

st.plotly_chart(fig6, use_container_width=True, config={'displayModeBar': False}) 

 

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

            <li>Address 2026-2028 high-risk period with enhanced monitoring</li> 

            <li>Implement real-time telemetry for supplier visibility</li> 

            <li>Establish automated KPI alert systems</li> 

            <li>Increase production capacity planning for peak demand years</li> 

        </ul> 

    </div> 

    """, unsafe_allow_html=True) 

     

    st.markdown(""" 

    <div class='alert-box success'> 

        <h4 style='margin-top: 0; color: #065f46;'>✅ Quick Wins</h4> 

        <ul style='margin-bottom: 0;'> 

            <li>Deploy predictive analytics dashboard</li> 

            <li>Integrate supplier portals with central system</li> 

            <li>Automate weekly risk & backlog reports</li> 

            <li>Implement early warning system for production gaps</li> 

        </ul> 

    </div> 

    """, unsafe_allow_html=True) 

 

with col2: 

    st.markdown(""" 

    <div class='alert-box'> 

        <h4 style='margin-top: 0; color: #92400e;'>📋 Long-term Strategy</h4> 

        <ul style='margin-bottom: 0;'> 

            <li>Build AI-powered capacity planning models</li> 

            <li>Expand oversight to tier-2/3 suppliers</li> 

            <li>Develop comprehensive supplier scorecards</li> 

            <li>Invest in predictive maintenance systems</li> 

            <li>Create digital twin for supply chain simulation</li> 

        </ul> 

    </div> 

    """, unsafe_allow_html=True) 

 

# ========================= 

# DATA TABLE 

# ========================= 

st.markdown("<h2 class='section-header'>📊 Detailed Data View</h2>", unsafe_allow_html=True) 

 

with st.expander("View Complete Dataset"): 

    # Create a styled dataframe 

    display_df = df_filtered.copy() 

     

    st.dataframe( 

        display_df, 

        use_container_width=True, 

        height=400 

    ) 

     

    # Download button 

    csv = df_filtered.to_csv(index=False).encode('utf-8') 

    st.download_button( 

        label="📥 Download Filtered Data", 

        data=csv, 

        file_name=f"boeing_oversight_data_{year_range[0]}-{year_range[1]}.csv", 

        mime="text/csv", 

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
