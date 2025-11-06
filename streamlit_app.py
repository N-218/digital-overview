
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
# CLEAN PROFESSIONAL STYLING
# =========================
st.markdown("""
<style>
    /* Clean white background */
    .stApp {
        background: #f8f9fa;
    }
    
    /* Boeing watermark - very subtle */
    .stApp::before {
        content: "";
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/3/36/Boeing_full_logo.svg");
        background-size: 20%;
        background-repeat: no-repeat;
        background-position: center;
        opacity: 0.02;
        position: fixed;
        top: 0; right: 0; bottom: 0; left: 0;
        z-index: 0;
        pointer-events: none;
    }
    
    /* Headers - dark readable text */
    h1, h2, h3 {
        color: #1a1a1a !important;
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        font-weight: 600;
    }
    
    h1 {
        font-size: 36px !important;
    }
    
    h2 {
        font-size: 24px !important;
        margin-top: 20px !important;
    }
    
    h3 {
        font-size: 18px !important;
        color: #2c3e50 !important;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #1a1a1a;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4a5568;
        font-weight: 600;
        font-size: 14px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 14px;
    }
    
    /* Sidebar - clean white */
    [data-testid="stSidebar"] {
        background: white;
        border-right: 2px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] label {
        color: #1a1a1a !important;
        font-weight: 500;
    }
    
    [data-testid="stSidebar"] h2 {
        color: #0066cc !important;
    }
    
    /* Remove excessive padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    
    /* Card styling */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        border-left: 4px solid #0066cc;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        font-weight: 600;
        color: #1a1a1a;
    }
    
    /* Better text readability */
    p, li, span {
        color: #2d3748;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR: Upload & Filters
# =========================
with st.sidebar:
    st.markdown("## 📂 Data Upload")
    uploaded_file = st.file_uploader(
        "Upload CSV File", 
        type=["csv"],
        help="Upload Digital_Oversight_Forecast.csv"
    )
    
    if uploaded_file is None:
        st.info("👆 Upload your CSV file to begin")
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
        (int(df["Year"].min()), int(df["Year"].max()))
    )
    
    risk_levels = st.multiselect(
        "Risk Levels",
        options=sorted(df["Risk_Level"].unique(), key=lambda x: risk_mapping[x]),
        default=df["Risk_Level"].unique()
    )
    
    st.markdown("---")
    st.markdown("### 📊 Summary")
    st.metric("Records", len(df))
    st.metric("Year Span", f"{df['Year'].max() - df['Year'].min() + 1}")

# Apply filters
df_filtered = df[
    (df["Year"] >= year_range[0]) & 
    (df["Year"] <= year_range[1]) &
    (df["Risk_Level"].isin(risk_levels))
]

# =========================
# CLEAN HEADER
# =========================
col_logo, col_title = st.columns([1, 4])

with col_logo:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #0066cc 0%, #004c99 100%); 
                padding: 30px; border-radius: 12px; text-align: center;'>
        <h1 style='color: white !important; margin: 0; font-size: 48px;'>✈️</h1>
    </div>
    """, unsafe_allow_html=True)

with col_title:
    st.markdown("""
    <div style='background: white; padding: 30px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-left: 5px solid #0066cc;'>
        <h1 style='margin: 0; color: #1a1a1a !important;'>Boeing Digital Oversight</h1>
        <p style='margin: 5px 0 0 0; font-size: 16px; color: #64748b;'>
            Production Forecast & Risk Analysis Dashboard
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# KPI METRICS ROW
# =========================
st.markdown("## 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_gap = df_filtered['Predicted_Gap'].sum()
max_risk = df_filtered['Risk_Score'].max()
high_risk_year = df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']
total_orders = df_filtered['Orders'].sum()

with col1:
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-top: 4px solid #0066cc;'>
        <p style='color: #64748b; font-size: 14px; margin: 0; font-weight: 600;'>PREDICTED GAP</p>
        <h2 style='color: #1a1a1a !important; margin: 10px 0 0 0; font-size: 36px;'>{:,.0f}</h2>
    </div>
    """.format(total_gap), unsafe_allow_html=True)

with col2:
    risk_color = "#ef4444" if max_risk == 3 else "#f59e0b" if max_risk == 2 else "#10b981"
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-top: 4px solid {};'>
        <p style='color: #64748b; font-size: 14px; margin: 0; font-weight: 600;'>MAX RISK LEVEL</p>
        <h2 style='color: #1a1a1a !important; margin: 10px 0 0 0; font-size: 36px;'>{}/3</h2>
    </div>
    """.format(risk_color, max_risk), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-top: 4px solid #8b5cf6;'>
        <p style='color: #64748b; font-size: 14px; margin: 0; font-weight: 600;'>CRITICAL YEAR</p>
        <h2 style='color: #1a1a1a !important; margin: 10px 0 0 0; font-size: 36px;'>{}</h2>
    </div>
    """.format(int(high_risk_year)), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-top: 4px solid #10b981;'>
        <p style='color: #64748b; font-size: 14px; margin: 0; font-weight: 600;'>TOTAL ORDERS</p>
        <h2 style='color: #1a1a1a !important; margin: 10px 0 0 0; font-size: 36px;'>{:,}</h2>
    </div>
    """.format(total_orders), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# INSIGHTS CARDS
# =========================
st.markdown("## 💡 Key Insights")

insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]
    if not high_gap_years.empty:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%); 
                    padding: 25px; border-radius: 12px; border-left: 5px solid #ef4444;'>
            <h3 style='color: #991b1b !important; margin: 0 0 10px 0;'>⚠️ High Gap Alert</h3>
            <p style='color: #7f1d1d; font-size: 16px; margin: 0; font-weight: 600;'>
                {len(high_gap_years)} years exceed threshold
            </p>
            <p style='color: #991b1b; font-size: 14px; margin: 10px 0 0 0;'>
                Years: {', '.join(map(str, high_gap_years['Year'].tolist()))}
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%); 
                    padding: 25px; border-radius: 12px; border-left: 5px solid #10b981;'>
            <h3 style='color: #065f46 !important; margin: 0 0 10px 0;'>✅ On Track</h3>
            <p style='color: #047857; font-size: 16px; margin: 0; font-weight: 600;'>
                All gaps within range
            </p>
            <p style='color: #065f46; font-size: 14px; margin: 10px 0 0 0;'>
                No critical interventions needed
            </p>
        </div>
        """, unsafe_allow_html=True)

with insight_col2:
    high_risk_count = len(df_filtered[df_filtered["Risk_Level"] == "High"])
    medium_risk_count = len(df_filtered[df_filtered["Risk_Level"] == "Medium"])
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%); 
                padding: 25px; border-radius: 12px; border-left: 5px solid #0066cc;'>
        <h3 style='color: #1e3a8a !important; margin: 0 0 10px 0;'>🎯 Risk Profile</h3>
        <p style='color: #1e40af; font-size: 16px; margin: 0; font-weight: 600;'>
            {high_risk_count} High | {medium_risk_count} Medium
        </p>
        <p style='color: #1e3a8a; font-size: 14px; margin: 10px 0 0 0;'>
            Active monitoring required
        </p>
    </div>
    """, unsafe_allow_html=True)

with insight_col3:
    avg_actual = df_filtered["ActualOutput"].mean()
    avg_planned = df_filtered["PlannedOutput"].mean()
    performance = (avg_actual / avg_planned * 100) if avg_planned > 0 else 0
    perf_color = "#10b981" if performance >= 95 else "#f59e0b" if performance >= 85 else "#ef4444"
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                padding: 25px; border-radius: 12px; border-left: 5px solid #f59e0b;'>
        <h3 style='color: #92400e !important; margin: 0 0 10px 0;'>📈 Performance</h3>
        <p style='color: #78350f; font-size: 16px; margin: 0; font-weight: 600;'>
            {performance:.1f}% of plan achieved
        </p>
        <p style='color: #92400e; font-size: 14px; margin: 10px 0 0 0;'>
            Actual vs Planned Output
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# CHARTS SECTION
# =========================
st.markdown("## 📈 Production Forecast & Risk Analysis")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("""
    <div style='background: white; padding: 20px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
    """, unsafe_allow_html=True)
    
    st.markdown("### Production Gap Forecast")
    
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["ProductionGap"],
        mode='lines+markers',
        name='Historical Gap',
        line=dict(color='#0066cc', width=3),
        marker=dict(size=10),
        hovertemplate='<b>Year</b>: %{x}<br><b>Historical</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig1.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["Predicted_Gap"],
        mode='lines+markers',
        name='Predicted Gap',
        line=dict(color='#ef4444', width=3, dash='dash'),
        marker=dict(size=10),
        hovertemplate='<b>Year</b>: %{x}<br><b>Predicted</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig1.update_layout(
        height=380,
        template="plotly_white",
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with chart_col2:
    st.markdown("""
    <div style='background: white; padding: 20px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
    """, unsafe_allow_html=True)
    
    st.markdown("### Risk Distribution by Year")
    
    color_map = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444"}
    
    fig2 = px.bar(
        df_filtered,
        x="Year",
        y="Risk_Score",
        color="Risk_Level",
        color_discrete_map=color_map,
        text="Risk_Level"
    )
    
    fig2.update_traces(textposition='outside')
    fig2.update_layout(
        height=380,
        template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# ROADMAP SECTION
# =========================
st.markdown("## 🗺️ Implementation Roadmap 2025")

st.markdown("""
<div style='background: white; padding: 30px; border-radius: 12px; 
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
""", unsafe_allow_html=True)

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
    'Planning': '#0066cc',
    'Implementation': '#10b981',
    'Integration': '#8b5cf6',
    'Analytics': '#f59e0b',
    'Dashboard': '#06b6d4',
    'Review': '#ef4444'
}

fig_roadmap = px.timeline(
    phases,
    x_start="Start",
    x_end="Finish",
    y="Phase",
    color="Category",
    color_discrete_map=colors
)

fig_roadmap.update_yaxes(autorange="reversed")
fig_roadmap.update_layout(
    height=320,
    template="plotly_white",
    showlegend=True,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=20, b=20),
    xaxis_title="2025 Timeline",
    yaxis_title="",
    plot_bgcolor='white',
    paper_bgcolor='white'
)

st.plotly_chart(fig_roadmap, use_container_width=True)

# Quarterly breakdown
roadmap_col1, roadmap_col2, roadmap_col3 = st.columns(3)

with roadmap_col1:
    st.markdown("""
    <div style='background: #eff6ff; padding: 20px; border-radius: 10px; border-left: 4px solid #0066cc;'>
        <h4 style='margin: 0 0 10px 0; color: #1e40af;'>Q1 2025: Foundation</h4>
        <ul style='font-size: 14px; margin: 0; padding-left: 20px; color: #1e3a8a;'>
            <li>Vendor selection</li>
            <li>Hardware procurement</li>
            <li>Team mobilization</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with roadmap_col2:
    st.markdown("""
    <div style='background: #ecfdf5; padding: 20px; border-radius: 10px; border-left: 4px solid #10b981;'>
        <h4 style='margin: 0 0 10px 0; color: #047857;'>Q2-Q3 2025: Build</h4>
        <ul style='font-size: 14px; margin: 0; padding-left: 20px; color: #065f46;'>
            <li>IoT sensor installation</li>
            <li>Supplier integration (50+)</li>
            <li>Pilot program launch</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with roadmap_col3:
    st.markdown("""
    <div style='background: #fef2f2; padding: 20px; border-radius: 10px; border-left: 4px solid #ef4444;'>
        <h4 style='margin: 0 0 10px 0; color: #991b1b;'>Q4 2025: Scale</h4>
        <ul style='font-size: 14px; margin: 0; padding-left: 20px; color: #7f1d1d;'>
            <li>Full dashboard rollout</li>
            <li>Performance evaluation</li>
            <li>Scale-up decision</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# DETAILED ANALYSIS
# =========================
st.markdown("## 📊 Detailed Production Analysis")

detail_col1, detail_col2 = st.columns(2)

with detail_col1:
    st.markdown("""
    <div style='background: white; padding: 20px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
    """, unsafe_allow_html=True)
    
    st.markdown("### Output vs Demand")
    
    fig3 = go.Figure()
    
    fig3.add_trace(go.Bar(
        x=df_filtered["Year"],
        y=df_filtered["PlannedOutput"],
        name='Planned',
        marker_color='#93c5fd',
        hovertemplate='<b>Planned</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig3.add_trace(go.Bar(
        x=df_filtered["Year"],
        y=df_filtered["ActualOutput"],
        name='Actual',
        marker_color='#0066cc',
        hovertemplate='<b>Actual</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig3.add_trace(go.Scatter(
        x=df_filtered["Year"],
        y=df_filtered["Orders"],
        name='Orders',
        mode='lines+markers',
        line=dict(color='#f59e0b', width=3),
        marker=dict(size=10),
        yaxis='y2',
        hovertemplate='<b>Orders</b>: %{y:,.0f}<extra></extra>'
    ))
    
    fig3.update_layout(
        height=360,
        template="plotly_white",
        barmode='group',
        yaxis2=dict(overlaying='y', side='right', title='Orders'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=60, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with detail_col2:
    st.markdown("""
    <div style='background: white; padding: 20px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
    """, unsafe_allow_html=True)
    
    st.markdown("### Backlog Trends")
    
    color_map_backlog = {"Low": "#10b981", "Medium": "#f59e0b", "High": "#ef4444"}
    
    fig4 = px.area(
        df_filtered,
        x="Year",
        y="Backlog",
        color="Risk_Level",
        color_discrete_map=color_map_backlog,
        line_shape='spline'
    )
    
    fig4.update_layout(
        height=360,
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=20, r=20, t=20, b=20),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# RECOMMENDATIONS
# =========================
st.markdown("## 🎯 Strategic Recommendations")

rec_col1, rec_col2 = st.columns([2.5, 1.5])

with rec_col1:
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);'>
    """, unsafe_allow_html=True)
    
    with st.expander("📌 **Immediate Actions Required**", expanded=True):
        high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]["Year"].tolist()
        if high_gap_years:
            st.markdown(f"""
            <div style='color: #1a1a1a;'>
            
            **🚨 Critical Alert:** High production gaps in years **{', '.join(map(str, high_gap_years))}**
            
            **Action Items:**
            - Deploy additional supplier oversight teams
            - Initiate emergency performance reviews
            - Implement enhanced quality controls
            - Accelerate digital monitoring deployment
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("✅ No immediate critical actions required")
        
        st.markdown("""
        **Strategic Priorities:**
        - Real-time telemetry monitoring
        - Automated KPI dashboards
        - Strengthen supplier partnerships
        - Capability development programs
        """)
    
    with st.expander("🗺️ **Medium-Term Strategy**"):
        st.markdown("""
        **Scale & Optimize:**
        - Scale to all Tier-1 suppliers by Q3 2025
        - Establish supplier excellence centers
        - Negotiate flexible capacity agreements
        - Invest in predictive analytics & AI
        - Launch supplier recognition program
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

with rec_col2:
    st.markdown("""
    <div style='background: white; padding: 25px; border-radius: 12px; 
                box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-top: 4px solid #0066cc;'>
        <h3 style='margin: 0 0 20px 0; color: #1a1a1a !important;'>📈 Expected Impact</h3>
        
        <div style='margin-bottom: 20px;'>
            <p style='color: #64748b; font-size: 13px; margin: 0; font-weight: 600;'>GAP REDUCTION</p>
            <p style='color: #10b981; font-size: 32px; margin: 5px 0 0 0; font-weight: 700;'>-25%</p>
            <p style='color: #64748b; font-size: 12px; margin: 0;'>by Q4 2025</p>
        </div>
        
        <div style='margin-bottom: 20px;'>
            <p style='color: #64748b; font-size: 13px; margin: 0; font-weight: 600;'>RISK DETECTION</p>
            <p style='color: #0066cc; font-size: 32px; margin: 5px 0 0 0; font-weight: 700;'>60%</p>
            <p style='color: #64748b; font-size: 12px; margin: 0;'>faster identification</p>
        </div>
        
        <div style='margin-bottom: 20px;'>
            <p style='color: #64748b; font-size: 13px; margin: 0; font-weight: 600;'>COST SAVINGS</p>
            <p style='color: #f59e0b; font-size: 32px; margin: 5px 0 0 0; font-weight: 700;'>$50M+</p>
            <p style='color: #64748b;
