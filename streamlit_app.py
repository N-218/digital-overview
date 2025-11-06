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
# CUSTOM STYLING
# =========================
st.markdown("""
<style>
    /* Modern gradient background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Boeing watermark */
    .stApp::before {
        content: "";
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/3/36/Boeing_full_logo.svg");
        background-size: 25%;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.03;
        position: fixed;
        top: 0; right: 0; bottom: 0; left: 0;
        z-index: 0;
        pointer-events: none;
    }
    
    /* Card styling for metrics */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
    }
    
    /* Headers */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
        color: #0a3d62;
    }
    
    h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white;
    }
    
    /* Remove extra spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 0rem;
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
# HEADER SECTION
# =========================
st.markdown("""
<div style='text-align: center; padding: 20px 0; background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 30px;'>
    <h1 style='margin: 0; font-size: 42px; color: #0a3d62;'>✈️ Boeing Digital Oversight Dashboard</h1>
    <p style='margin: 10px 0 0 0; font-size: 18px; color: #7f8c8d;'>Executive Summary | Production Forecast & Risk Analysis</p>
</div>
""", unsafe_allow_html=True)

# =========================
# EXECUTIVE KPIs
# =========================
st.markdown("## 🎯 Executive Summary")

col1, col2, col3, col4, col5 = st.columns(5)

total_gap = df_filtered['Predicted_Gap'].sum()
max_risk = df_filtered['Risk_Score'].max()
high_risk_year = df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']
total_orders = df_filtered['Orders'].sum()
avg_backlog = df_filtered['Backlog'].mean()

col1.metric(
    "Total Predicted Gap", 
    f"{total_gap:,.0f}",
    help="Total forecasted production gap"
)
col2.metric(
    "Maximum Risk Level", 
    f"{'🔴' if max_risk == 3 else '🟡' if max_risk == 2 else '🟢'} {max_risk}/3",
    help="Highest risk score in filtered period"
)
col3.metric(
    "Critical Year", 
    f"{int(high_risk_year)}",
    delta="⚠️ Highest Risk",
    help="Year with maximum risk exposure"
)
col4.metric(
    "Total Orders", 
    f"{total_orders:,}",
    help="Cumulative orders in period"
)
col5.metric(
    "Avg Backlog", 
    f"{avg_backlog:,.0f}",
    help="Average backlog across period"
)

st.markdown("---")

# =========================
# KEY INSIGHTS CARDS
# =========================
st.markdown("## 💡 Key Insights")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]
    if not high_gap_years.empty:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%); padding: 20px; border-radius: 10px; color: white;'>
            <h3 style='color: white; margin-top: 0;'>⚠️ High Gap Alert</h3>
            <p style='font-size: 16px;'><strong>{len(high_gap_years)} years</strong> show gaps exceeding 300 units</p>
            <p style='font-size: 14px; opacity: 0.9;'>Years: {', '.join(map(str, high_gap_years['Year'].tolist()))}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); padding: 20px; border-radius: 10px; color: white;'>
            <h3 style='color: white; margin-top: 0;'>✅ On Track</h3>
            <p style='font-size: 16px;'>All gaps within acceptable range</p>
            <p style='font-size: 14px; opacity: 0.9;'>No critical interventions needed</p>
        </div>
        """, unsafe_allow_html=True)

with insight_col2:
    high_risk_count = len(df_filtered[df_filtered["Risk_Level"] == "High"])
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; color: white;'>
        <h3 style='color: white; margin-top: 0;'>🎯 Risk Profile</h3>
        <p style='font-size: 16px;'><strong>{high_risk_count}</strong> high-risk periods identified</p>
        <p style='font-size: 14px; opacity: 0.9;'>Requires immediate attention</p>
    </div>
    """, unsafe_allow_html=True)

with insight_col3:
    avg_actual = df_filtered["ActualOutput"].mean()
    avg_planned = df_filtered["PlannedOutput"].mean()
    performance = (avg_actual / avg_planned * 100) if avg_planned > 0 else 0
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; color: white;'>
        <h3 style='color: white; margin-top: 0;'>📈 Performance</h3>
        <p style='font-size: 16px;'>Avg Output: <strong>{performance:.1f}%</strong> of plan</p>
        <p style='font-size: 14px; opacity: 0.9;'>Actual vs Planned Output</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================
# MAIN VISUALIZATIONS
# =========================
st.markdown("## 📊 Production Forecast & Risk Analysis")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("### Production Gap Trend")
    
    fig1 = go.Figure()
    
    # Add actual gap
    fig1.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["ProductionGap"],
        mode='lines+markers',
        name='Historical Gap',
        line=dict(color='#3498db', width=3),
        marker=dict(size=8),
        hovertemplate='<b>Year</b>: %{x}<br><b>Gap</b>: %{y:,.0f}<extra></extra>'
    ))
    
    # Add predicted gap
    fig1.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["Predicted_Gap"],
        mode='lines+markers',
        name='Predicted Gap',
        line=dict(color='#e74c3c', width=3, dash='dash'),
        marker=dict(size=8),
        hovertemplate='<b>Year</b>: %{x}<br><b>Predicted</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig1.update_layout(
        height=400,
        template="plotly_white",
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    st.markdown("### Risk Distribution by Year")
    
    color_map = {"Low": "#2ecc71", "Medium": "#f39c12", "High": "#e74c3c"}
    
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
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# DETAILED BREAKDOWN
# =========================
st.markdown("---")
st.markdown("## 📋 Detailed Production Breakdown")

breakdown_col1, breakdown_col2 = st.columns(2)

with breakdown_col1:
    st.markdown("### Output vs Demand")
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(
        x=df_filtered["Year"],
        y=df_filtered["PlannedOutput"],
        name='Planned Output',
        marker_color='#3498db',
        hovertemplate='<b>Planned</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig3.add_trace(go.Bar(
        x=df_filtered["Year"],
        y=df_filtered["ActualOutput"],
        name='Actual Output',
        marker_color='#2ecc71',
        hovertemplate='<b>Actual</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig3.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["Orders"],
        name='Orders',
        mode='lines+markers',
        line=dict(color='#e74c3c', width=3),
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
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig3, use_container_width=True)

with breakdown_col2:
    st.markdown("### Backlog Analysis")
    
    fig4 = px.area(
        df_filtered,
        x="Year",
        y="Backlog",
        color="Risk_Level",
        color_discrete_map=color_map,
        line_shape='spline'
    )
    
    fig4.update_layout(
        height=400,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    st.plotly_chart(fig4, use_container_width=True)

# =========================
# RECOMMENDATIONS
# =========================
st.markdown("---")
st.markdown("## 🎯 Strategic Recommendations")

rec_col1, rec_col2 = st.columns([2, 1])

with rec_col1:
    with st.expander("📌 **Immediate Actions Required**", expanded=True):
        high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]["Year"].tolist()
        if high_gap_years:
            st.markdown(f"""
            - 🚨 **Critical Alert**: High production gaps in years {', '.join(map(str, high_gap_years))}
            - ⚡ Deploy additional supplier oversight teams immediately
            - 📞 Initiate emergency supplier performance reviews
            """)
        else:
            st.markdown("- ✅ No immediate critical actions required")
        
        st.markdown("""
        - 🔍 Implement real-time digital telemetry monitoring
        - 📊 Create automated KPI dashboards for supplier performance
        - 🤝 Strengthen partnerships with high-performing suppliers
        """)
    
    with st.expander("🗺️ **Medium-Term Strategy**"):
        st.markdown("""
        - 📈 Scale digital oversight platform to all Tier-1 suppliers by Q3 2025
        - 🎓 Establish supplier training programs for quality consistency
        - 💼 Negotiate flexible capacity agreements with backup suppliers
        - 🔬 Invest in predictive analytics capabilities
        """)

with rec_col2:
    st.markdown("### 📈 Expected Impact")
    st.markdown("""
    <div style='background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
        <p><strong>Gap Reduction:</strong><br/>
        <span style='font-size: 24px; color: #2ecc71;'>-25%</span> by Q4 2025</p>
        
        <p><strong>Risk Mitigation:</strong><br/>
        <span style='font-size: 24px; color: #3498db;'>60%</span> faster detection</p>
        
        <p><strong>Cost Savings:</strong><br/>
        <span style='font-size: 24px; color: #f39c12;'>$50M+</span> annually</p>
    </div>
    """, unsafe_allow_html=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 20px; color: #7f8c8d;'>
    <p style='margin: 0;'><strong>Boeing Digital Oversight Initiative</strong> | Confidential Board Presentation</p>
    <p style='margin: 5px 0 0 0; font-size: 14px;'>Last Updated: November 2025 | Data Source: Digital_Oversight_Forecast.csv</p>
</div>
""", unsafe_allow_html=True)
