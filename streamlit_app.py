import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ================================
# PAGE CONFIG
# ================================
st.set_page_config(
    page_title="Boeing Digital Oversight Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================
# SIDEBAR: Upload & Filters
# ================================
st.sidebar.title("📂 Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload Digital_Oversight_Forecast.csv", type=["csv"]
)

if uploaded_file is None:
    st.info("👆 Please upload your CSV file to begin")
    st.stop()

df = pd.read_csv(uploaded_file)

# Map Risk_Level to numeric score
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# ================================
# Filters
# ================================
st.sidebar.markdown("---")
st.sidebar.header("🔍 Filters")

year_range = st.sidebar.slider(
    "Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

risk_levels = st.sidebar.multiselect(
    "Risk Levels",
    options=sorted(df["Risk_Level"].unique(), key=lambda x: risk_mapping[x]),
    default=df["Risk_Level"].unique()
)

df_filtered = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1]) &
    (df["Risk_Level"].isin(risk_levels))
]

# ================================
# HEADER
# ================================
st.markdown("""
<div style="text-align:center">
    <h1 style="color:#146FD7">✈️ BOEING</h1>
    <h2>Digital Oversight Dashboard</h2>
    <h4 style="color:#767676">Production Forecast & Risk Analysis</h4>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ================================
# EXECUTIVE KPIs
# ================================
st.subheader("🎯 Executive Summary")
col1, col2, col3, col4 = st.columns(4)

total_gap = df_filtered['Predicted_Gap'].sum()
max_risk = df_filtered['Risk_Score'].max()
high_risk_year = df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']
total_orders = df_filtered['Orders'].sum()

col1.metric("Total Predicted Gap", f"{total_gap:,.0f}")
col2.metric("Maximum Risk Level", f"{max_risk}/3", delta="⚠️" if max_risk == 3 else "✓")
col3.metric("Critical Year", f"{int(high_risk_year)}", delta="Priority Focus")
col4.metric("Total Orders", f"{total_orders:,}")

st.markdown("---")

# ================================
# KEY INSIGHTS
# ================================
st.subheader("💡 Key Insights")
insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]
    if not high_gap_years.empty:
        st.markdown(f"""
        ⚠️ **High Gap Alert**  
        {len(high_gap_years)} years show critical gaps  
        Years: {', '.join(map(str, high_gap_years['Year'].tolist()))}
        """)
    else:
        st.markdown("✅ On Track – All gaps within acceptable range")

with insight_col2:
    high_risk_count = len(df_filtered[df_filtered["Risk_Level"] == "High"])
    medium_risk_count = len(df_filtered[df_filtered["Risk_Level"] == "Medium"])
    st.markdown(f"""
    🎯 **Risk Profile**  
    {high_risk_count} High | {medium_risk_count} Medium  
    Active monitoring required
    """)

with insight_col3:
    avg_actual = df_filtered["ActualOutput"].mean()
    avg_planned = df_filtered["PlannedOutput"].mean()
    performance = (avg_actual / avg_planned * 100) if avg_planned > 0 else 0
    st.markdown(f"""
    📈 **Performance**  
    {performance:.1f}% of plan achieved  
    Actual vs Planned Output
    """)

st.markdown("---")

# ================================
# FORECAST & RISK CHARTS
# ================================
st.subheader("📊 Forecast and Risk Overview")
chart_col1, chart_col2 = st.columns(2)

boeing_blue = '#146FD7'
boeing_red = '#E2545B'
boeing_gray = '#767676'

with chart_col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["ProductionGap"],
        mode='lines+markers',
        name='Historical Gap',
        line=dict(color=boeing_blue, width=3),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>Historical Gap: %{y:,.0f}'
    ))
    fig1.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["Predicted_Gap"],
        mode='lines+markers',
        name='Predicted Gap',
        line=dict(color=boeing_red, width=3, dash='dash'),
        marker=dict(size=8),
        hovertemplate='Year: %{x}<br>Predicted Gap: %{y:,.0f}'
    ))
    fig1.update_layout(
        height=360,
        template="plotly_white",
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1),
        margin=dict(l=12, r=0, t=8, b=0),
        plot_bgcolor='#fff',
        paper_bgcolor='#fff'
    )
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    color_map = {"Low": "#6ac27d", "Medium": "#ffbb33", "High": "#E2545B"}
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
        height=360,
        template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.04, xanchor="right", x=1),
        margin=dict(l=8, r=0, t=8, b=0),
        plot_bgcolor='#fff',
        paper_bgcolor='#fff'
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ================================
# IMPLEMENTATION ROADMAP
# ================================
st.subheader("🗺️ Implementation Roadmap 2025")
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

colors = {
    'Planning': '#0033a0', 'Implementation': '#2e7d32', 'Integration': '#6a1b9a',
    'Analytics': '#f57c00', 'Dashboard': '#00796b', 'Review': '#c41e3a'
}

fig_roadmap = px.timeline(
    phases, x_start="Start", x_end="Finish", y="Phase", color="Category",
    color_discrete_map=colors, title="2025 Digital Oversight Implementation Timeline"
)
fig_roadmap.update_yaxes(autorange="reversed")
fig_roadmap.update_layout(
    height=350, template="plotly_white", showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=0, r=0, t=40, b=0), title_x=0.5,
    title_font=dict(size=18, color='#0033a0', family='Helvetica Neue'),
    xaxis_title="Timeline", yaxis_title="", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_roadmap, use_container_width=True)

# ================================
# STRATEGIC RECOMMENDATIONS
# ================================
st.subheader("🎯 Strategic Recommendations")
rec_col1, rec_col2 = st.columns([2, 1])

with rec_col1:
    with st.expander("📌 Immediate Actions Required", expanded=True):
        high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]["Year"].tolist()
        if high_gap_years:
            st.markdown(f"""
            - 🚨 Critical Alert: High production gaps in years {', '.join(map(str, high_gap_years))}
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
    with st.expander("🗺️ Medium-Term Strategy"):
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
    **Gap Reduction:** -25% by Q4 2025  
    **Risk Detection:** 60% faster identification  
    **Cost Savings:** $50M+ annually projected  
    **Supplier Performance:** +15% improvement target
    """)

# ================================
# FOOTER
# ================================
st.markdown("---")
st.markdown("""
<small>BOEING DIGITAL OVERSIGHT INITIATIVE | Confidential Board Presentation | Last Updated: November 2025</small>
""", unsafe_allow_html=True)
