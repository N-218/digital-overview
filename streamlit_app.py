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
# CUSTOM CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&family=Roboto+Condensed:wght@400;700&display=swap');

.stApp { background: #f0f2f5; font-family: 'Roboto', sans-serif; }
.block-container { padding-top: 2rem; padding-bottom: 2rem; }

.dashboard-header { 
    background: linear-gradient(135deg, #0033A0 0%, #005EB8 100%);
    padding: 2.5rem 3rem; border-radius: 0; margin: -2rem -3rem 2rem -3rem;
    box-shadow: 0 4px 12px rgba(0, 51, 160, 0.2);
}

.header-content { display: flex; justify-content: space-between; align-items: center; max-width: 1400px; margin: 0 auto; }
.header-left h1 { color: white; font-family: 'Roboto Condensed', sans-serif; font-size: 2.8rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
.header-left p { color: #b8d4f0; font-size: 1.15rem; margin-top: 0.5rem; font-weight: 400; }
.boeing-logo { font-family: 'Roboto Condensed', sans-serif; color: white; font-size: 3rem; font-weight: 700; letter-spacing: 8px; }

.section-header { color: #0033A0; font-family: 'Roboto Condensed', sans-serif; font-size: 1.75rem; font-weight: 700; 
                  margin: 3rem 0 1.5rem 0; padding-bottom: 0.75rem; border-bottom: 3px solid #0033A0; letter-spacing: -0.5px; }

.metric-card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
               border-left: 4px solid #0033A0; margin-bottom: 1rem; transition: all 0.3s ease; cursor: pointer; }
.metric-card:hover { box-shadow: 0 4px 16px rgba(0, 51, 160, 0.2); transform: translateY(-2px); }
.metric-label { font-size: 0.875rem; color: #64748b; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 0.5rem; }
.metric-value { font-size: 2.25rem; color: #0f172a; font-weight: 700; line-height: 1; margin-bottom: 0.5rem; }
.metric-delta { font-size: 0.875rem; color: #64748b; font-weight: 500; }

.alert-box { padding: 1.5rem; border-radius: 8px; margin: 1.5rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.alert-box.critical { background: #fef2f2; border-left: 5px solid #dc2626; }
.alert-box.success { background: #f0fdf4; border-left: 5px solid #10b981; }
.alert-box.info { background: #eff6ff; border-left: 5px solid #3b82f6; }
.alert-box h4 { font-size: 1.1rem; font-weight: 600; margin-top: 0; margin-bottom: 0.75rem; }
.alert-box ul { margin: 0; padding-left: 1.5rem; }
.alert-box li { margin-bottom: 0.5rem; line-height: 1.6; font-size: 0.95rem; }

.risk-item { margin-bottom: 1.25rem; padding: 1rem; background: white; border-radius: 6px; }
.risk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.risk-label { font-weight: 600; font-size: 1rem; color: #0f172a; }
.risk-count { font-weight: 700; font-size: 1.1rem; }
.risk-bar-bg { background: #e2e8f0; border-radius: 10px; height: 12px; overflow: hidden; }
.risk-bar-fill { height: 100%; border-radius: 10px; transition: width 0.3s ease; }

.phase-card { text-align: center; padding: 1.5rem 1rem; background: white; border-radius: 8px;
              box-shadow: 0 2px 8px rgba(0,0,0,0.08); border-top: 3px solid #0033A0; transition: all 0.3s ease; }
.phase-card:hover { transform: translateY(-3px); box-shadow: 0 4px 16px rgba(0, 51, 160, 0.2); }
.phase-progress { font-size: 2.5rem; font-weight: 700; color: #0033A0; line-height: 1; }
.phase-label { font-size: 0.875rem; color: #64748b; margin-top: 0.5rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }

.dashboard-footer { text-align: center; padding: 2.5rem 0 1.5rem 0; border-top: 2px solid #e2e8f0; margin-top: 3rem; }
.footer-title { color: #0f172a; font-size: 0.95rem; font-weight: 600; margin: 0; }
.footer-meta { color: #94a3b8; font-size: 0.8rem; margin-top: 0.5rem; }

.chart-container { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1.5rem; }

.stButton>button { background: #0033A0; color: white; border: none; border-radius: 6px; padding: 0.5rem 1.5rem; 
                   font-weight: 600; transition: all 0.3s ease; }
.stButton>button:hover { background: #005EB8; box-shadow: 0 4px 12px rgba(0, 51, 160, 0.3); }

.stTabs [data-baseweb="tab-list"] { gap: 8px; }
.stTabs [data-baseweb="tab"] { background-color: white; border-radius: 8px 8px 0 0; padding: 1rem 2rem; font-weight: 600; }
.stTabs [aria-selected="true"] { background-color: #0033A0; color: white; }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR: UPLOAD OR DEFAULT
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

# =========================
# LOAD DATA
# =========================
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("No file uploaded — loading default dataset")
    df = pd.DataFrame({
        "Year": [2021,2022,2023,2024,2025,2026,2027,2028],
        "PlannedOutput": [264,372,456,456,456,0,0,0],
        "ActualOutput": [263,387,396,265,45,0,0,0],
        "Orders": [395,626,1075,236,558,0,0,0],
        "Backlog": [3414,3653,4332,4303,4816,0,0,0],
        "ProductionGap": [1,-15,60,191,411,0,0,0],
        "Backlog_Change_Pct": [0,0.07,0.186,-0.007,0.119,0,0,0],
        "NetLoss": [-459.2,-546,-633,-476.9,-724.3,0,0,0],
        "ForwardLosses": [-227.3,0,0,-217,-585,0,0,0],
        "ExcessCapacityCost": [-206.7,0,0,-70,-55,0,0,0],
        "Risk_Level": ["Low","Low","Medium","Medium","High","High","High","High"],
        "Predicted_Gap": [-75.6,27,129.6,232.2,334.8,437.4,540,642.6]
    })

# =========================
# RISK SCORE MAPPING
# =========================
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# =========================
# SIDEBAR FILTERS
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
    gap_threshold = st.slider("Show Gaps Greater Than", 0, int(df["Predicted_Gap"].max()), 0, step=10, key="gap_filter")
    
    st.markdown("#### 📦 Order Volume")
    order_min, order_max = st.slider("Order Range", int(df["Orders"].min()), int(df["Orders"].max()),
                                     (int(df["Orders"].min()), int(df["Orders"].max())), key="order_filter")
    
    st.markdown("---")
    st.markdown("#### ⚡ Quick Filters")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚨 High Risk", use_container_width=True):
            st.session_state.risk_filter = ["High"]
            st.experimental_rerun()
    with col2:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.risk_filter = df['Risk_Level'].unique().tolist()
            st.experimental_rerun()

# =========================
# APPLY FILTERS
# =========================
df_filtered = df[
    (df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1]) &
    (df["Risk_Level"].isin(risk_levels)) &
    (df["Predicted_Gap"] >= gap_threshold) &
    (df["Orders"] >= order_min) & (df["Orders"] <= order_max)
]

if df_filtered.empty:
    st.warning("⚠️ No data matches your filter criteria. Showing full dataset instead.")
    df_filtered = df.copy()

# =========================
# METRICS
# =========================
col1, col2, col3, col4 = st.columns(4)

total_gap = df_filtered['Predicted_Gap'].sum()
total_orders = df_filtered['Orders'].sum()
avg_orders = df_filtered['Orders'].mean() if len(df_filtered) > 0 else 0
high_risk_count = len(df_filtered[df_filtered['Risk_Level'] == 'High'])

if len(df_filtered) > 0 and df_filtered['Risk_Score'].sum() > 0:
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
# CHARTS & TABS
# =========================
st.markdown("<div class='section-header'>📈 Production vs Orders</div>", unsafe_allow_html=True)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(x=df_filtered["Year"], y=df_filtered["Orders"], name="Orders", marker_color="#0033A0"))
fig.add_trace(go.Line(x=df_filtered["Year"], y=df_filtered["ActualOutput"], name="Actual Output", marker_color="#10B981"), secondary_y=False)
fig.add_trace(go.Line(x=df_filtered["Year"], y=df_filtered["PlannedOutput"], name="Planned Output", marker_color="#F59E0B"), secondary_y=False)
fig.add_trace(go.Line(x=df_filtered["Year"], y=df_filtered["Predicted_Gap"], name="Predicted Gap", marker_color="#DC2626", line=dict(dash="dot")), secondary_y=True)

fig.update_layout(barmode='group', legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
fig.update_yaxes(title_text="Units Produced / Ordered", secondary_y=False)
fig.update_yaxes(title_text="Predicted Gap", secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

# =========================
# RISK DASHBOARD
# =========================
st.markdown("<div class='section-header'>⚡ Risk Overview</div>", unsafe_allow_html=True)

risk_summary = df_filtered.groupby("Risk_Level").size().reset_index(name="Count")
for _, row in risk_summary.iterrows():
    width = min(100, row["Count"]*10)
    st.markdown(f"""
    <div class='risk-item'>
        <div class='risk-header'>
            <div class='risk-label'>{row['Risk_Level']}</div>
            <div class='risk-count'>{row['Count']}</div>
        </div>
        <div class='risk-bar-bg'><div class='risk-bar-fill' style='width:{width}%;background-color:#0033A0'></div></div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# ROADMAP & RECOMMENDATIONS
# =========================
st.markdown("<div class='section-header'>🛣️ Roadmap & Recommendations</div>", unsafe_allow_html=True)

st.markdown("""
<div class='phase-card'>
    <div class='phase-progress'>1️⃣</div>
    <div class='phase-label'>Short-term: Stabilize Production</div>
    <p>Optimize capacity planning, reallocate resources, and reduce predicted gaps.</p>
</div>
<br>
<div class='phase-card'>
    <div class='phase-progress'>2️⃣</div>
    <div class='phase-label'>Mid-term: Mitigate High-Risk Years</div>
    <p>Engage suppliers, enhance monitoring, and implement early-warning systems.</p>
</div>
<br>
<div class='phase-card'>
    <div class='phase-progress'>3️⃣</div>
    <div class='phase-label'>Long-term: Strategic Forecasting</div>
    <p>Invest in predictive analytics, automate backlog management, and reduce production volatility.</p>
</div>
""", unsafe_allow_html=True)

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
