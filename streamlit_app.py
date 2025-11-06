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
    transition: all 0.3s ease;
    cursor: pointer;
}

.metric-card:hover {
    box-shadow: 0 4px 16px rgba(0, 51, 160, 0.2);
    transform: translateY(-2px);
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
    transition: all 0.3s ease;
}

.phase-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 16px rgba(0, 51, 160, 0.2);
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

/* Chart Container */
.chart-container {
    background: white;
    padding: 1.5rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
}

/* Interactive Elements */
.stButton>button {
    background: #0033A0;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background: #005EB8;
    box-shadow: 0 4px 12px rgba(0, 51, 160, 0.3);
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}

.stTabs [data-baseweb="tab"] {
    background-color: white;
    border-radius: 8px 8px 0 0;
    padding: 1rem 2rem;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    background-color: #0033A0;
    color: white;
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

# =========================
# INTERACTIVE SIDEBAR FILTERS
# =========================
with st.sidebar:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### 🔍 Interactive Filters")
    
    # Year Range Slider
    year_range = st.slider(
        "Year Range", 
        int(df["Year"].min()), 
        int(df["Year"].max()), 
        (int(df["Year"].min()), int(df["Year"].max())),
        key="year_filter"
    )
    
    # Risk Level Multi-select
    risk_levels = st.multiselect(
        "Risk Levels", 
        df["Risk_Level"].unique(), 
        default=df["Risk_Level"].unique(),
        key="risk_filter"
    )
    
    # Gap Threshold Slider
    st.markdown("---")
    st.markdown("#### 📊 Gap Analysis")
    gap_threshold = st.slider(
        "Show Gaps Greater Than",
        0,
        int(df["Predicted_Gap"].max()),
        0,
        step=100,
        key="gap_filter"
    )
    
    # Order Range Filter
    st.markdown("#### 📦 Order Volume")
    order_min, order_max = st.slider(
        "Order Range",
        int(df["Orders"].min()),
        int(df["Orders"].max()),
        (int(df["Orders"].min()), int(df["Orders"].max())),
        key="order_filter"
    )
    
    # Quick Filter Buttons
    st.markdown("---")
    st.markdown("#### ⚡ Quick Filters")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 High Risk Only", use_container_width=True):
            st.session_state.risk_filter = ["High"]
            st.rerun()
    with col2:
        if st.button("🔄 Reset All", use_container_width=True):
            st.session_state.year_filter = (int(df["Year"].min()), int(df["Year"].max()))
            st.session_state.risk_filter = list(df["Risk_Level"].unique())
            st.session_state.gap_filter = 0
            st.session_state.order_filter = (int(df["Orders"].min()), int(df["Orders"].max()))
            st.rerun()

# Apply all filters
df_filtered = df[
    (df["Year"] >= year_range[0]) & 
    (df["Year"] <= year_range[1]) &
    (df["Risk_Level"].isin(risk_levels)) &
    (df["Predicted_Gap"] >= gap_threshold) &
    (df["Orders"] >= order_min) &
    (df["Orders"] <= order_max)
]

# Show filter status
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
# INTERACTIVE KEY METRICS
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
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Total Predicted Gap</div>
        <div class='metric-value'>{total_gap:,.0f}</div>
        <div class='metric-delta'>{(total_gap/total_orders*100 if total_orders > 0 else 0):.1f}% of total orders</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>High-Risk Periods</div>
        <div class='metric-value'>{high_risk_count}</div>
        <div class='metric-delta'>{(high_risk_count/len(df_filtered)*100 if len(df_filtered) > 0 else 0):.0f}% of timeline</div>
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
# INTERACTIVE TABBED ANALYSIS
# =========================
st.markdown("<h2 class='section-header'>ANALYSIS VIEWS</h2>", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📈 Production Trends", "🎯 Correlation Analysis", "📊 Risk Breakdown", "🗓️ Year-by-Year"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        
        # Chart type selector
        chart_type = st.radio(
            "Chart Type:",
            ["Line Chart", "Area Chart", "Bar Chart"],
            horizontal=True,
            key="prod_chart_type"
        )
        
        fig1 = go.Figure()
        
        if chart_type == "Line Chart":
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
        
        elif chart_type == "Area Chart":
            fig1.add_trace(go.Scatter(
                x=df_filtered['Year'], 
                y=df_filtered['ProductionGap'], 
                name='Actual Gap',
                mode='lines',
                line=dict(color='#94a3b8', width=2),
                fill='tozeroy',
                fillcolor='rgba(148, 163, 184, 0.3)'
            ))
            
            fig1.add_trace(go.Scatter(
                x=df_filtered['Year'], 
                y=df_filtered['Predicted_Gap'], 
                name='Predicted Gap',
                mode='lines',
                line=dict(color='#0033A0', width=3),
                fill='tozeroy',
                fillcolor='rgba(0, 51, 160, 0.3)'
            ))
        
        else:  # Bar Chart
            fig1.add_trace(go.Bar(
                x=df_filtered['Year'], 
                y=df_filtered['ProductionGap'], 
                name='Actual Gap',
                marker_color='#94a3b8'
            ))
            
            fig1.add_trace(go.Bar(
                x=df_filtered['Year'], 
                y=df_filtered['Predicted_Gap'], 
                name='Predicted Gap',
                marker_color='#0033A0'
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

with tab2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        scatter_color = st.selectbox(
            "Color by:",
            ["Risk Level", "Year"],
            key="scatter_color"
        )
    with col2:
        scatter_size = st.selectbox(
            "Size by:",
            ["Risk Score", "Orders", "Predicted Gap"],
            key="scatter_size"
        )
    
    if scatter_color == "Risk Level":
        color_col = df_filtered['Risk_Score']
        colorscale = [[0, '#10b981'], [0.5, '#f59e0b'], [1, '#dc2626']]
    else:
        color_col = df_filtered['Year']
        colorscale = 'Viridis'
    
    if scatter_size == "Risk Score":
        size_col = df_filtered['Risk_Score'] * 12
    elif scatter_size == "Orders":
        size_col = df_filtered['Orders'] / 100
    else:
        size_col = df_filtered['Predicted_Gap'] / 50
    
    fig_scatter = go.Figure()
    
    fig_scatter.add_trace(go.Scatter(
        x=df_filtered['Orders'],
        y=df_filtered['Predicted_Gap'],
        mode='markers',
        marker=dict(
            size=size_col,
            color=color_col,
            colorscale=colorscale,
            showscale=True,
            colorbar=dict(title=scatter_color)
        ),
        text=df_filtered['Year'],
        hovertemplate='<b>Year %{text}</b><br>Orders: %{x:,}<br>Predicted Gap: %{y:,}<extra></extra>',
        name='Year Data'
    ))
    
    fig_scatter.update_layout(
        title=dict(text='Orders vs Predicted Gap Analysis', font=dict(size=16, weight=600)),
        xaxis_title='Orders',
        yaxis_title='Predicted Gap',
        template='plotly_white',
        height=500,
        hovermode='closest'
    )
    
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Risk Distribution by Count")
        risk_counts = df_filtered['Risk_Level'].value_counts()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=risk_counts.index,
            values=risk_counts.values,
            marker=dict(colors=['#dc2626', '#f59e0b', '#10b981']),
            hole=0.4,
            textinfo='label+percent',
            textfont=dict(size=14, weight=600)
        )])
        
        fig_pie.update_layout(
            height=400,
            showlegend=True,
            template='plotly_white'
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("#### Gap by Risk Level")
        gap_by_risk = df_filtered.groupby('Risk_Level')['Predicted_Gap'].sum().reset_index()
        
        fig_bar = go.Figure(data=[go.Bar(
            x=gap_by_risk['Risk_Level'],
            y=gap_by_risk['Predicted_Gap'],
            marker_color=['#10b981', '#f59e0b', '#dc2626'],
            text=gap_by_risk['Predicted_Gap'],
            texttemplate='%{text:,.0f}',
            textposition='outside'
        )])
        
        fig_bar.update_layout(
            height=400,
            xaxis_title='Risk Level',
            yaxis_title='Total Predicted Gap',
            template='plotly_white',
            showlegend=False
        )
        
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    
    # Year selector for drill-down
    selected_year = st.selectbox(
        "Select Year for Detailed View:",
        df_filtered['Year'].unique(),
        key="year_select"
    )
    
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
    
    # Historical comparison
    st.markdown("#### Historical Comparison")
    
    fig_compare = go.Figure()
    
    fig_compare.add_trace(go.Bar(
        x=df_filtered['Year'],
        y=df_filtered['Orders'],
        name='Orders',
        marker_color='#0033A0',
        yaxis='y'
    ))
    
    fig_compare.add_trace(go.Scatter(
        x=df_filtered['Year'],
        y=df_filtered['Predicted_Gap'],
        name='Predicted Gap',
        mode='lines+markers',
        marker=dict(size=10, color='#dc2626'),
        line=dict(width=3, color='#dc2626'),
        yaxis='y2'
    ))
    
    fig_compare.update_layout(
        height=400,
        template='plotly_white',
        yaxis=dict(title='Orders'),
        yaxis2=dict(title='Predicted Gap', overlaying='y', side='right'),
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig_compare, use_container_width=True)
    
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

# Interactive phase selector
selected_phase = st.selectbox("Select Phase for Details:", phases['Phase'].tolist())
phase_info = phases[phases['Phase'] == selected_phase].iloc[0]

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Progress", f"{phase_info['Progress']}%")
with col2:
    st.metric("Start Date", phase_info['Start'].strftime('%Y-%m-%d'))
with col3:
    st.metric("End Date", phase_info['Finish'].strftime('%Y-%m-%d'))

colors = {
    'Planning': '#0033A0',
