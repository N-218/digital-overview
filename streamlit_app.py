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

# PROFESSIONAL BLUE & WHITE STYLING  

# =========================  

st.markdown("""  

<style>  

    /* Clean white background */  

    .stApp {  

        background: #f8f9fc; 

    }  

      

    /* Content cards with subtle shadow */  

    .content-card {  

        background: white;  

        padding: 30px;  

        border-radius: 16px;  

        box-shadow: 0 2px 8px rgba(0,0,0,0.08);  

        margin-bottom: 24px; 

        border: 1px solid #e8edf2; 

    }  

      

    /* Professional blue headers */  

    h1, h2, h3 {  

        color: #1e3a5f !important;  

        font-family: 'Inter', 'Segoe UI', Arial, sans-serif;  

        font-weight: 600;  

    }  

      

    /* Metric cards with better contrast */  

    [data-testid="stMetricValue"] {  

        font-size: 32px;  

        font-weight: 700;  

        color: #1e3a5f;  

    }  

      

    [data-testid="stMetricLabel"] {  

        color: #6b7c93;  

        font-weight: 500; 

        font-size: 14px; 

    }  

      

    /* Clean sidebar */  

    [data-testid="stSidebar"] {  

        background: #ffffff; 

        border-right: 1px solid #e8edf2; 

    }  

      

    [data-testid="stSidebar"] .stMarkdown,   

    [data-testid="stSidebar"] label {  

        color: #1e3a5f !important; 

        font-weight: 500; 

    }  

      

    /* Optimized padding */  

    .block-container {  

        padding-top: 2rem;  

        padding-bottom: 1rem;  

        max-width: 100%;  

    }  

      

    /* Modern button styling */  

    .stButton > button {  

        background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%); 

        color: white;  

        border: none;  

        border-radius: 8px;  

        font-weight: 600; 

        padding: 12px 24px; 

        transition: all 0.3s ease; 

    } 

     

    .stButton > button:hover { 

        transform: translateY(-2px); 

        box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3); 

    } 

      

    /* Clean expander */  

    .streamlit-expanderHeader {  

        background-color: #f8f9fc;  

        border-radius: 8px;  

        font-weight: 600;  

        color: #1e3a5f; 

        border: 1px solid #e8edf2; 

    } 

     

    /* Remove default streamlit branding colors */ 

    .css-1v0mbdj.etr89bj1 { 

        color: #1e3a5f; 

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

# HEADER SECTION - CLEAN & PROFESSIONAL  

# =========================  

st.markdown("""  

<div style='background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%); padding: 40px 30px; border-radius: 16px; box-shadow: 0 4px 16px rgba(74, 144, 226, 0.25); margin-bottom: 30px;'>  

    <div style='text-align: center;'>  

        <h1 style='margin: 0; font-size: 48px; color: white; font-weight: 700; letter-spacing: -1px;'>✈️ BOEING</h1>  

        <h2 style='margin: 12px 0; font-size: 28px; color: white; font-weight: 400;'>Digital Oversight Dashboard</h2>  

        <p style='margin: 8px 0 0 0; font-size: 14px; color: rgba(255,255,255,0.9); letter-spacing: 2px; text-transform: uppercase;'>Production Forecast & Risk Analysis</p>  

    </div>  

</div>  

""", unsafe_allow_html=True)  

 

# =========================  

# EXECUTIVE KPIs - CLEAN CARDS  

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

# KEY INSIGHTS - PROFESSIONAL CARDS  

# =========================  

st.markdown("<div class='content-card'>", unsafe_allow_html=True)  

st.markdown("## 💡 Key Insights")  

 

insight_col1, insight_col2, insight_col3 = st.columns(3)  

 

with insight_col1:  

    high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]  

    if not high_gap_years.empty:  

        st.markdown(f"""  

        <div style='background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(255, 107, 107, 0.25);'>  

            <h3 style='color: white; margin-top: 0; font-size: 20px;'>⚠️ High Gap Alert</h3>  

            <p style='font-size: 32px; margin: 12px 0; font-weight: 700;'>{len(high_gap_years)} years</p>  

            <p style='font-size: 13px; opacity: 0.95; margin: 0;'>Years: {', '.join(map(str, high_gap_years['Year'].tolist()))}</p>  

        </div>  

        """, unsafe_allow_html=True)  

    else:  

        st.markdown("""  

        <div style='background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(81, 207, 102, 0.25);'>  

            <h3 style='color: white; margin-top: 0; font-size: 20px;'>✅ On Track</h3>  

            <p style='font-size: 32px; margin: 12px 0; font-weight: 700;'>All Clear</p>  

            <p style='font-size: 13px; opacity: 0.95; margin: 0;'>No critical interventions needed</p>  

        </div>  

        """, unsafe_allow_html=True)  

 

with insight_col2:  

    high_risk_count = len(df_filtered[df_filtered["Risk_Level"] == "High"])  

    medium_risk_count = len(df_filtered[df_filtered["Risk_Level"] == "Medium"])  

    st.markdown(f"""  

    <div style='background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(74, 144, 226, 0.25);'>  

        <h3 style='color: white; margin-top: 0; font-size: 20px;'>🎯 Risk Profile</h3>  

        <p style='font-size: 32px; margin: 12px 0; font-weight: 700;'>{high_risk_count} High | {medium_risk_count} Med</p>  

        <p style='font-size: 13px; opacity: 0.95; margin: 0;'>Active monitoring required</p>  

    </div>  

    """, unsafe_allow_html=True)  

 

with insight_col3:  

    avg_actual = df_filtered["ActualOutput"].mean()  

    avg_planned = df_filtered["PlannedOutput"].mean()  

    performance = (avg_actual / avg_planned * 100) if avg_planned > 0 else 0  

    st.markdown(f"""  

    <div style='background: linear-gradient(135deg, #ffa94d 0%, #fd7e14 100%); padding: 24px; border-radius: 12px; color: white; box-shadow: 0 4px 12px rgba(255, 169, 77, 0.25);'>  

        <h3 style='color: white; margin-top: 0; font-size: 20px;'>📈 Performance</h3>  

        <p style='font-size: 32px; margin: 12px 0; font-weight: 700;'>{performance:.1f}%</p>  

        <p style='font-size: 13px; opacity: 0.95; margin: 0;'>Actual vs Planned Output</p>  

    </div>  

    """, unsafe_allow_html=True)  

 

st.markdown("</div>", unsafe_allow_html=True)  

 

# =========================  

# FORECAST & RISK CHARTS  

# =========================  

st.markdown("<div class='content-card'>", unsafe_allow_html=True)  

st.markdown("## 📊 Forecast and Risk Overview")  

 

chart_col1, chart_col2 = st.columns(2)  

 

with chart_col1:  

    st.markdown("### Production Gap Forecast")  

      

    fig1 = go.Figure()  

      

    fig1.add_trace(go.Scatter(  

        x=df_filtered["Year"],  

        y=df_filtered["ProductionGap"],  

        mode='lines+markers',  

        name='Historical Gap',  

        line=dict(color='#4a90e2', width=3),  

        marker=dict(size=10, color='#4a90e2'),  

        hovertemplate='<b>Year</b>: %{x}<br><b>Historical Gap</b>: %{y:,.0f}<extra></extra>'  

    ))  

      

    fig1.add_trace(go.Scatter(  

        x=df_filtered["Year"],  

        y=df_filtered["Predicted_Gap"],  

        mode='lines+markers',  

        name='Predicted Gap',  

        line=dict(color='#ff6b6b', width=3, dash='dash'),  

        marker=dict(size=10, color='#ff6b6b'),  

        hovertemplate='<b>Year</b>: %{x}<br><b>Predicted Gap</b>: %{y:,.0f}<extra></extra>'  

    ))  

      

    fig1.update_layout(  

        height=400,  

        template="plotly_white",  

        hovermode='x unified',  

        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),  

        margin=dict(l=0, r=0, t=10, b=0),  

        plot_bgcolor='white',  

        paper_bgcolor='white', 

        font=dict(family='Inter, sans-serif', color='#1e3a5f') 

    )  

      

    st.plotly_chart(fig1, use_container_width=True)  

 

with chart_col2:  

    st.markdown("### Risk Levels by Year")  

      

    color_map = {"Low": "#51cf66", "Medium": "#ffa94d", "High": "#ff6b6b"}  

      

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

        plot_bgcolor='white',  

        paper_bgcolor='white', 

        font=dict(family='Inter, sans-serif', color='#1e3a5f') 

    )  

      

    st.plotly_chart(fig2, use_container_width=True)  

 

st.markdown("</div>", unsafe_allow_html=True)  

 

# =========================  

# IMPLEMENTATION ROADMAP  

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

 

# Professional blue palette 

colors = {  

    'Planning': '#4a90e2',  

    'Implementation': '#51cf66',  

    'Integration': '#9775fa',  

    'Analytics': '#ffa94d',  

    'Dashboard': '#20c997',  

    'Review': '#ff6b6b'  

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

    title_font=dict(size=18, color='#1e3a5f', family='Inter'),  

    xaxis_title="Timeline",  

    yaxis_title="",  

    plot_bgcolor='white',  

    paper_bgcolor='white', 

    font=dict(family='Inter, sans-serif', color='#1e3a5f') 

)  

 

st.plotly_chart(fig_roadmap, use_container_width=True)  

 

# Roadmap milestones  

st.markdown("### Implementation Phases")  

roadmap_col1, roadmap_col2, roadmap_col3 = st.columns(3)  

 

with roadmap_col1:  

    st.markdown("""  

    <div style='background: #f8f9fc; padding: 24px; border-radius: 12px; border-left: 4px solid #4a90e2;'>  

        <h4 style='margin-top: 0; color: #1e3a5f;'>Q1 2025: Foundation</h4>  

        <ul style='font-size: 14px; margin: 10px 0; color: #6b7c93; line-height: 1.8;'>  

            <li><strong style='color: #1e3a5f;'>Planning & Vendor Setup</strong></li>  

            <li>Vendor selection completed</li>  

            <li>Hardware procurement initiated</li>  

            <li>Project team mobilized</li>  

        </ul>  

    </div>  

    """, unsafe_allow_html=True)  

 

with roadmap_col2:  

    st.markdown("""  

    <div style='background: #f8f9fc; padding: 24px; border-radius: 12px; border-left: 4px solid #51cf66;'>  

        <h4 style='margin-top: 0; color: #1e3a5f;'>Q2-Q3 2025: Build</h4>  

        <ul style='font-size: 14px; margin: 10px 0; color: #6b7c93; line-height: 1.8;'>  

            <li><strong style='color: #1e3a5f;'>Implementation & Integration</strong></li>  

            <li>Install IoT sensors network</li>  

            <li>Integrate 50+ suppliers</li>  

            <li>Launch pilot & analytics</li>  

        </ul>  

    </div>  

    """, unsafe_allow_html=True)  

 

with roadmap_col3:  

    st.markdown("""  

    <div style='background: #f8f9fc; padding: 24px; border-radius: 12px; border-left: 4px solid #ff6b6b;'>  

        <h4 style='margin-top: 0; color: #1e3a5f;'>Q4 2025: Scale</h4>  

        <ul style='font-size: 14px; margin: 10px 0; color: #6b7c93; line-height: 1.8;'>  

            <li><strong style='color: #1e3a5f;'>Deployment & Review</strong></li>  

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

        marker_color='#4a90e2',  

        hovertemplate='<b>Planned</b>: %{y:,.0f}<extra></extra>'  

    ))  

      

    fig3.add_trace(go.Bar(  

        x=df_filtered["Year"],  

        y=df_filtered["ActualOutput"],  

        name='Actual Output',  

        marker_color='#51cf66',  

        hovertemplate='<b>Actual</b>: %{y:,.0f}<extra></extra>'  

    ))  

      

    fig3.add_trace(go.Scatter(  

        x=df_filtered["Year"],  

        y=df_filtered["Orders"],  

        name='Orders',  

        mode='lines+markers',  

        line=dict(color='#ff6b6b', width=3),  

        marker=dict(size=10, color='#ff6b6b'),  

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

        plot_bgcolor='white',  

        paper_bgcolor='white', 

        font=dict(family='Inter, sans-serif', color='#1e3a5f') 

    )  

      

    st.plotly_chart(fig3, use_container_width=True)  

 

with breakdown_col2:  

    st.markdown("### Backlog Trends")  

      

    color_map_backlog = {"Low": "#51cf66", "Medium": "#ffa94d", "High": "#ff6b6b"}  

      

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

        plot_bgcolor='white',  

        paper_bgcolor='white', 

        font=dict(family='Inter, sans-serif', color='#1e3a5f') 

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

    <div style='background: #f8f9fc; padding: 24px; border-radius: 12px; border: 2px solid #4a90e2;'>  

        <p style='margin: 12px 0;'><strong style='color: #1e3a5f;'>Gap Reduction:</strong><br/>  

        <span style='font-size: 36px; color: #51cf66; font-weight: 700;'>-25%</span><br/>  

        <span style='font-size: 13px; color: #6b7c93;'>by Q4 2025</span></p>  

          

        <p style='margin: 12px 0;'><strong style='color: #1e3a5f;'>Risk Detection:</strong><br/>  

        <span style='font-size: 36px; color: #4a90e2; font-weight: 700;'>60%</span><br/>  

        <span style='font-size: 13px; color: #6b7c93;'>faster identification</span></p>  

          

        <p style='margin: 12px 0;'><strong style='color: #1e3a5f;'>Cost Savings:</strong><br/>  

        <span style='font-size: 36px; color: #ffa94d; font-weight: 700;'>$50M+</span><br/>  

        <span style='font-size: 13px; color: #6b7c93;'>annually projected</span></p>  

          

        <p style='margin: 12px 0;'><strong style='color: #1e3a5f;'>Supplier Performance:</strong><br/>  

        <span style='font-size: 36px; color: #9775fa; font-weight: 700;'>+15%</span><br/>  

        <span style='font-size: 13px; color: #6b7c93;'>improvement target</span></p>  

    </div>  

    """, unsafe_allow_html=True)  

 

st.markdown("</div>", unsafe_allow_html=True)  

 

# =========================  

# FOOTER - CLEAN PROFESSIONAL  

# =========================  

st.markdown("""  

<div style='background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%); padding: 30px; border-radius: 12px; margin-top: 30px; text-align: center; color: white; box-shadow: 0 4px 16px rgba(74, 144, 226, 0.25);'>  

    <p style='margin: 0; font-size: 16px; font-weight: 600; letter-spacing: 2px;'>BOEING DIGITAL OVERSIGHT INITIATIVE</p>  

    <p style='margin: 8px 0 0 0; font-size: 13px; opacity: 0.9;'>Confidential Board Presentation | Last Updated: November 2025</p>  

</div>  

""", unsafe_allow_html=True) 
