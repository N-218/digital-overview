import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
# BOEING BRAND STYLING
# =========================
st.markdown("""
<style>
    /* Boeing branded gradient background */
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #003d7a 50%, #0066cc 100%);
    }
    
    /* Boeing watermark */
    .stApp::before {
        content: "";
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/3/36/Boeing_full_logo.svg");
        background-size: 30%;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.04;
        position: fixed;
        top: 0; right: 0; bottom: 0; left: 0;
        z-index: 0;
        pointer-events: none;
    }
    
    /* Content cards with white background */
    .content-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    /* Boeing blue headers */
    h1, h2, h3 {
        color: #0033a0 !important;
        font-family: 'Helvetica Neue', Arial, sans-serif;
        font-weight: 700;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #0033a0;
    }
    
    [data-testid="stMetricLabel"] {
        color: #003d7a;
        font-weight: 600;
    }
    
    /* Sidebar Boeing theme */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #001f3f 0%, #003d7a 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label {
        color: white !important;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #0033a0;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: 600;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f0f4f8;
        border-radius: 8px;
        font-weight: 600;
        color: #0033a0;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR: Upload & Filters
# =========================
with st.sidebar:
    st.markdown("## 📂 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload Digital_Oversight_Forecast.csv", 
        type=["csv"],
        help="Upload your forecast CSV file"
    )
    
    if uploaded_file is None:
        st.info("👆 Please upload your CSV file to begin")
        st.stop()
    
    df = pd.read_csv(uploaded_file)
    
    # Data processing
    risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
    df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)
    
    st.markdown("---")
    st.markdown("## 🔍 Filters")
    
    year_range = st.slider(
        "Year Range",
        int(df["Year"].min()),
        int(df["Year"].max()),
        (int(df["Year"].min()), int(df["Year"].max())),
        help="Filter data by year range"
    )
    
    risk_levels = st.multiselect(
        "Risk Levels",
        options=sorted(df["Risk_Level"].unique(), key=lambda x: risk_mapping[x]),
        default=df["Risk_Level"].unique(),
        help="Select which risk levels to display"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Data Summary")
    st.metric("Total Records", len(df))
    st.metric("Years Covered", f"{df['Year'].min()} - {df['Year'].max()}")

# Apply filters
df_filtered = df[
    (df["Year"] >= year_range[0]) & 
    (df["Year"] <= year_range[1]) &
    (df["Risk_Level"].isin(risk_levels))
]

# =========================
# HEADER SECTION - BOEING STYLE
# =========================
st.markdown("""
<div style='background: white; padding: 30px 20px; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 25px; border-top: 5px solid #0033a0;'>
    <div style='text-align: center;'>
        <h1 style='margin: 0; font-size: 44px; color: #0033a0;'>✈️ BOEING</h1>
        <h2 style='margin: 10px 0; font-size: 32px; color: #003d7a;'>Digital Oversight Dashboard</h2>
        <p style='margin: 5px 0 0 0; font-size: 16px; color: #666; letter-spacing: 1px;'>PRODUCTION FORECAST & RISK ANALYSIS</p>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# EXECUTIVE KPIs - BOEING THEME
# =========================
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("## 🎯 Executive Summary")

col1, col2, col3, col4 = st.columns(4)

total_gap = df_filtered['Predicted_Gap'].sum()
max_risk = df_filtered['Risk_Score'].max()
high_risk_year = df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']
total_orders = df_filtered['Orders'].sum()

col1.metric(
    "Total Predicted Gap", 
    f"{total_gap:,.0f}",
    help="Total forecasted production gap"
)
col2.metric(
    "Maximum Risk Level", 
    f"{max_risk}/3",
    delta="⚠️" if max_risk == 3 else "✓",
    help="Highest risk score in filtered period"
)
col3.metric(
    "Critical Year", 
    f"{int(high_risk_year)}",
    delta="Priority Focus",
    help="Year with maximum risk exposure"
)
col4.metric(
    "Total Orders", 
    f"{total_orders:,}",
    help="Cumulative orders in period"
)
st.markdown("</div>", unsafe_allow_html=True)

# =========================
# KEY INSIGHTS - BOEING COLORS
# =========================
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("## 💡 Key Insights")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]
    if not high_gap_years.empty:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #c41e3a 0%, #8b0000 100%); padding: 20px; border-radius: 10px; color: white;'>
            <h3 style='color: white; margin-top: 0;'>⚠️ High Gap Alert</h3>
            <p style='font-size: 18px; margin: 10px 0;'><strong>{len(high_gap_years)} years</strong> show critical gaps</p>
            <p style='font-size: 14px; opacity: 0.9; margin: 0;'>Years: {', '.join(map(str, high_gap_years['Year'].tolist()))}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%); padding: 20px; border-radius: 10px; color: white;'>
            <h3 style='color: white; margin-top: 0;'>✅ On Track</h3>
            <p style='font-size: 18px; margin: 10px 0;'>All gaps within acceptable range</p>
            <p style='font-size: 14px; opacity: 0.9; margin: 0;'>No critical interventions needed</p>
        </div>
        """, unsafe_allow_html=True)

with insight_col2:
    high_risk_count = len(df_filtered[df_filtered["Risk_Level"] == "High"])
    medium_risk_count = len(df_filtered[df_filtered["Risk_Level"] == "Medium"])
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #0033a0 0%, #001f3f 100%); padding: 20px; border-radius: 10px; color: white;'>
        <h3 style='color: white; margin-top: 0;'>🎯 Risk Profile</h3>
        <p style='font-size: 18px; margin: 10px 0;'><strong>{high_risk_count}</strong> High | <strong>{medium_risk_count}</strong> Medium</p>
        <p style='font-size: 14px; opacity: 0.9; margin: 0;'>Active monitoring required</p>
    </div>
    """, unsafe_allow_html=True)

with insight_col3:
    avg_actual = df_filtered["ActualOutput"].mean()
    avg_planned = df_filtered["PlannedOutput"].mean()
    performance = (avg_actual / avg_planned * 100) if avg_planned > 0 else 0
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f57c00 0%, #e65100 100%); padding: 20px; border-radius: 10px; color: white;'>
        <h3 style='color: white; margin-top: 0;'>📈 Performance</h3>
        <p style='font-size: 18px; margin: 10px 0;'><strong>{performance:.1f}%</strong> of plan achieved</p>
        <p style='font-size: 14px; opacity: 0.9; margin: 0;'>Actual vs Planned Output</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FORECAST & RISK CHARTS
# =========================
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("## 📊 Forecast and Risk Overview")

chart_col1, chart_col2 = st.columns(2)

# Boeing color palette
boeing_blue = '#0033a0'
boeing_red = '#c41e3a'
boeing_gray = '#767676'

with chart_col1:
    st.markdown("### Production Gap Forecast")
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["ProductionGap"],
        mode='lines+markers',
        name='Historical Gap',
        line=dict(color=boeing_blue, width=3),
        marker=dict(size=10),
        hovertemplate='<b>Year</b>: %{x}<br><b>Historical Gap</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig1.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["Predicted_Gap"],
        mode='lines+markers',
        name='Predicted Gap',
        line=dict(color=boeing_red, width=3, dash='dash'),
        marker=dict(size=10),
        hovertemplate='<b>Year</b>: %{x}<br><b>Predicted Gap</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig1.update_layout(
        height=400,
        template="plotly_white",
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    st.markdown("### Risk Levels by Year")
    
    color_map = {"Low": "#2e7d32", "Medium": "#f57c00", "High": "#c41e3a"}
    
    fig2 = px.bar(
        df_filtered,
        x="Year",
        y="Risk_Score",
        color="Risk_Level",
        color_discrete_map=color_map,
        text="Risk_Level",
        hover_data=["Predicted_Gap", "Backlog"]
    )
    
    fig2.update_traces(textposition='outside')
    fig2.update_layout(
        height=400,
        template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# IMPLEMENTATION ROADMAP - BOEING STYLE
# =========================
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("## 🗺️ Implementation Roadmap 2025")

# Create roadmap data
phases = pd.DataFrame([
    dict(Phase='Planning & Vendor Setup', Start='2025-01-01', Finish='2025-02-28', Category='Planning'),
    dict(Phase='Telemetry Installation', Start='2025-03-01', Finish='2025-04-30', Category='Implementation'),
    dict(Phase='Supplier Integration', Start='2025-05-01', Finish='2025-06-30', Category='Integration'),
    dict(Phase='Pilot & Analytics', Start='2025-07-01', Finish='2025-09-30', Category='Analytics'),
    dict(Phase='Dashboard Deployment', Start='2025-10-01', Finish='2025-11-30', Category='Dashboard'),
    dict(Phase='Review & Scale Decision', Start='2025-12-01', Finish='2025-12-31', Category='Review')
])

phases["Start"] = pd.to_datetime(phases["Start"])
phases["Finish"] = pd.to_datetime(phases["Finish"])

# Boeing themed colors for roadmap
colors = {
    'Planning': '#0033a0',
    'Implementation': '#2e7d32',
    'Integration': '#6a1b9a',
    'Analytics': '#f57c00',
    'Dashboard': '#00796b',
    'Review': '#c41e3a'
}

fig_roadmap = px.timeline(
    phases,
    x_start="Start",
    x_end="Finish",
    y="Phase",
    color="Category",
    color_discrete_map=colors,
    title="2025 Digital Oversight Implementation Timeline"
)

fig_roadmap.update_yaxes(autorange="reversed")
fig_roadmap.update_layout(
    height=350,
    template="plotly_white",
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=40, b=0),
    title_x=0.5,
    title_font=dict(size=18, color='#0033a0', family='Helvetica Neue'),
    xaxis_title="Timeline",
    yaxis_title="",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)

st.plotly_chart(fig_roadmap, use_container_width=True)

# Roadmap milestones
st.markdown("### Implementation Phases")
roadmap_col1, roadmap_col2, roadmap_col3 = st.columns(3)

with roadmap_col1:
    st.markdown("""
    <div style='background: #f0f4f8; padding: 20px; border-radius: 8px; border-left: 5px solid #0033a0;'>
        <h4 style='margin-top: 0; color: #0033a0;'>Q1 2025: Foundation</h4>
        <ul style='font-size: 14px; margin: 10px 0; color: #333;'>
            <li><strong>Planning & Vendor Setup</strong></li>
            <li>Vendor selection completed</li>
            <li>Hardware procurement initiated</li>
            <li>Project team mobilized</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with roadmap_col2:
    st.markdown("""
    <div style='background: #f0f4f8; padding: 20px; border-radius: 8px; border-left: 5px solid #2e7d32;'>
        <h4 style='margin-top: 0; color: #2e7d32;'>Q2-Q3 2025: Build</h4>
        <ul style='font-size: 14px; margin: 10px 0; color: #333;'>
            <li><strong>Implementation & Integration</strong></li>
            <li>Install IoT sensors network</li>
            <li>Integrate 50+ suppliers</li>
            <li>Launch pilot & analytics</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with roadmap_col3:
    st.markdown("""
    <div style='background: #f0f4f8; padding: 20px; border-radius: 8px; border-left: 5px solid #c41e3a;'>
        <h4 style='margin-top: 0; color: #c41e3a;'>Q4 2025: Scale</h4>
        <ul style='font-size: 14px; margin: 10px 0; color: #333;'>
            <li><strong>Deployment & Review</strong></li>
            <li>Full dashboard rollout</li>
            <li>Performance evaluation</li>
            <li>Scale-up decision point</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# DETAILED BREAKDOWN
# =========================
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("## 📋 Production Analysis")

breakdown_col1, breakdown_col2 = st.columns(2)

with breakdown_col1:
    st.markdown("### Output vs Demand Analysis")
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(
        x=df_filtered["Year"],
        y=df_filtered["PlannedOutput"],
        name='Planned Output',
        marker_color='#0066cc',
        hovertemplate='<b>Planned</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig3.add_trace(go.Bar(
        x=df_filtered["Year"],
        y=df_filtered["ActualOutput"],
        name='Actual Output',
        marker_color='#2e7d32',
        hovertemplate='<b>Actual</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig3.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["Orders"],
        name='Orders',
        mode='lines+markers',
        line=dict(color='#c41e3a', width=3),
        marker=dict(size=10),
        yaxis='y2',
        hovertemplate='<b>Orders</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig3.update_layout(
        height=400,
        template="plotly_white",
        barmode='group',
        yaxis2=dict(overlaying='y', side='right', title='Orders'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig3, use_container_width=True)

with breakdown_col2:
    st.markdown("### Backlog Trends")
    
    color_map_backlog = {"Low": "#2e7d32", "Medium": "#f57c00", "High": "#c41e3a"}
    
    fig4 = px.area(
        df_filtered,
        x="Year",
        y="Backlog",
        color="Risk_Level",
        color_discrete_map=color_map_backlog,
        line_shape='spline'
    )
    
    fig4.update_layout(
        height=400,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=10, b=0),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# STRATEGIC RECOMMENDATIONS
# =========================
st.markdown("<div class='content-card'>", unsafe_allow_html=True)
st.markdown("## 🎯 Strategic Recommendations")

rec_col1, rec_col2 = st.columns([2, 1])

with rec_col1:
    with st.expander("📌 **Immediate Actions Required**", expanded=True):
        high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]["Year"].tolist()
        if high_gap_years:
            st.markdown(f"""
            - 🚨 **Critical Alert**: High production gaps in years **{', '.join(map(str, high_gap_years))}**
            - ⚡ Deploy additional supplier oversight teams immediately
            - 📞 Initiate emergency supplier performance reviews
            - 🔍 Implement enhanced quality control measures
            """)
        else:
            st.markdown("- ✅ No immediate critical actions required")
        
        st.markdown("""
        - 📡 Implement real-time digital telemetry monitoring
        - 📊 Deploy automated KPI dashboards for suppliers
        - 🤝 Strengthen partnerships with high-performing suppliers
        - 🎓 Initiate supplier capability development programs
        """)
    
    with st.expander("🗺️ **Medium-Term Strategy**"):
        st.markdown("""
        - 📈 Scale digital oversight to all Tier-1 suppliers by Q3 2025
        - 🎯 Establish supplier excellence centers
        - 💼 Negotiate flexible capacity agreements
        - 🔬 Invest in predictive analytics and AI capabilities
        - 🏆 Launch supplier recognition program
        """)

with rec_col2:
    st.markdown("### 📈 Expected Impact")
    st.markdown("""
    <div style='background: #f0f4f8; padding: 20px; border-radius: 10px; border: 2px solid #0033a0;'>
        <p style='margin: 10px 0;'><strong style='color: #0033a0;'>Gap Reduction:</strong><br/>
        <span style='font-size: 28px; color: #2e7d32; font-weight: 700;'>-25%</span><br/>
        <span style='font-size: 13px; color: #666;'>by Q4 2025</span></p>
        
        <p style='margin: 10px 0;'><strong style='color: #0033a0;'>Risk Detection:</strong><br/>
        <span style='font-size: 28px; color: #0033a0; font-weight: 700;'>60%</span><br/>
        <span style='font-size: 13px; color: #666;'>faster identification</span></p>
        
        <p style='margin: 10px 0;'><strong style='color: #0033a0;'>Cost Savings:</strong><br/>
        <span style='font-size: 28px; color: #f57c00; font-weight: 700;'>$50M+</span><br/>
        <span style='font-size: 13px; color: #666;'>annually projected</span></p>
        
        <p style='margin: 10px 0;'><strong style='color: #0033a0;'>Supplier Performance:</strong><br/>
        <span style='font-size: 28px; color: #6a1b9a; font-weight: 700;'>+15%</span><br/>
        <span style='font-size: 13px; color: #666;'>improvement target</span></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# FOOTER - BOEING BRANDED
# =========================
st.markdown("""
<div style='background: linear-gradient(90deg, #0033a0 0%, #001f3f 100%); padding: 25px; border-radius: 12px; margin-top: 20px; text-align: center; color: white;'>
    <p style='margin: 0; font-size: 16px; font-weight: 600; letter-spacing: 1px;'>BOEING DIGITAL OVERSIGHT INITIATIVE</p>
    <p style='margin: 5px 0 0 0; font-size: 13px; opacity: 0.8;'>Confidential Board Presentation | Last Updated: November 2025</p>
</div>
""", unsafe_allow_html=True)
