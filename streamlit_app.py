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
# CUSTOM CSS
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

.stApp { background: #f8fafc; font-family: 'Inter', 'Segoe UI', sans-serif; }

.dashboard-header { background: linear-gradient(135deg, #003087 0%, #0052CC 100%);
                    padding: 2rem; border-radius: 12px; margin-bottom: 2rem;
                    box-shadow: 0 4px 20px rgba(0, 48, 135, 0.15); width: 100%; }

.dashboard-title { color: white; font-size: 2.5rem; font-weight: 700; margin: 0; }
.dashboard-subtitle { color: #a8c5e8; font-size: 1.1rem; margin-top: 0.5rem; }

.metric-card { background: white; padding: 1.5rem; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);
               border-left: 4px solid #003087; transition: transform 0.2s, box-shadow 0.2s; }

.metric-card:hover { transform: translateY(-2px); box-shadow: 0 4px 16px rgba(0,0,0,0.12); }

.metric-label { color: #64748b; font-size: 0.875rem; font-weight: 500; text-transform: uppercase; margin-bottom: 0.5rem; }
.metric-value { color: #003087; font-size: 2rem; font-weight: 700; line-height: 1; }

.logo-space { text-align: right; color: white; font-weight: 600; font-size: 1.5rem; letter-spacing: 2px; }

.section-header { color: #003087; font-size: 1.5rem; font-weight: 600; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0; }

.alert-box { padding: 1rem 1.5rem; border-radius: 8px; margin: 1rem 0; }
.alert-box.critical { background: #fee2e2; border-left: 4px solid #dc2626; }
.alert-box.success { background: #d1fae5; border-left: 4px solid #10b981; }
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

# =========================
# LOAD DATA
# =========================
df = pd.read_csv(uploaded_file)
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# =========================
# SIDEBAR FILTERS
# =========================
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

# Apply filters once
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]

# =========================
# HEADER
# =========================
with st.container():
    st.markdown(f"""
    <div class='dashboard-header'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <h1 class='dashboard-title'>Digital Oversight Dashboard</h1>
                <p class='dashboard-subtitle'>Supply Chain Intelligence & Risk Management System</p>
            </div>
            <div class='logo-space'>✈️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# KEY METRICS
# =========================
with st.container():
    col1, col2, col3, col4 = st.columns(4)
    total_gap = df_filtered['Predicted_Gap'].sum()
    total_orders = df_filtered['Orders'].sum()
    avg_orders = df_filtered['Orders'].mean()
    high_risk_count = len(df_filtered[df_filtered['Risk_Level'] == 'High'])
    critical_year_row = df_filtered.loc[df_filtered['Risk_Score'].idxmax()]

    col1.metric("Total Predicted Gap", f"{total_gap:,.0f}", delta=f"{(total_gap/total_orders*100):.1f}% of orders")
    col2.metric("High-Risk Periods", high_risk_count, delta=f"{(high_risk_count/len(df_filtered)*100):.0f}% of timeline")
    col3.metric("Critical Year", critical_year_row['Year'], delta=f"Gap: {critical_year_row['Predicted_Gap']:,}")
    col4.metric("Total Orders", f"{total_orders:,}", delta=f"Avg: {avg_orders:.0f}/yr")

# =========================
# ALERT
# =========================
high_risk_years = df_filtered[df_filtered['Risk_Level'] == 'High']['Year'].tolist()
if high_risk_years:
    st.markdown(f"""
    <div class='alert-box critical'>
        <strong>⚠️ Critical Alert:</strong> High-risk periods detected in years: <strong>{', '.join(map(str, high_risk_years))}</strong>
        <br>Immediate action required for supplier oversight and capacity planning.
    </div>
    """, unsafe_allow_html=True)

# =========================
# GRAPHS
# =========================
with st.container():
    st.markdown("<h2 class='section-header'>📈 Production Analysis & Forecasting</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3,2])

    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df_filtered['Year'], y=df_filtered['ProductionGap'], name='Actual Gap', mode='lines+markers', line=dict(color='#94a3b8', width=3), marker=dict(size=8)))
        fig1.add_trace(go.Scatter(x=df_filtered['Year'], y=df_filtered['Predicted_Gap'], name='Predicted Gap', mode='lines+markers', line=dict(color='#003087', width=4), marker=dict(size=10, symbol='diamond')))
        fig1.update_layout(title='Production Gap: Actual vs Predicted', xaxis_title='Year', yaxis_title='Gap (Units)', template='plotly_white', height=400)
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    with col2:
        risk_counts = df_filtered['Risk_Level'].value_counts()
        st.markdown("#### Risk Distribution")
        for level in ['High', 'Medium', 'Low']:
            if level in risk_counts.index:
                count = risk_counts[level]
                perc = (count / len(df_filtered)) * 100
                color = {'High': '#dc2626', 'Medium': '#f59e0b', 'Low': '#10b981'}[level]
                st.markdown(f"""
                <div style='margin-bottom:0.5rem;'>
                    <div style='display:flex; justify-content:space-between;'><span>{level}</span><span style='color:{color}; font-weight:600'>{count} ({perc:.0f}%)</span></div>
                    <div style='background:#e2e8f0; border-radius:10px; height:8px;'><div style='width:{perc}%; background:{color}; height:100%; border-radius:10px;'></div></div>
                </div>
                """, unsafe_allow_html=True)

# =========================
# ORDERS vs GAP
# =========================
with st.container():
    st.markdown("<h2 class='section-header'>🎯 Orders & Gap Correlation</h2>", unsafe_allow_html=True)
    fig2 = make_subplots(rows=1, cols=2, subplot_titles=('Orders vs Predicted Gap', 'Year-over-Year Risk Progression'), specs=[[{"secondary_y": False}, {"type": "bar"}]])
    fig2.add_trace(go.Scatter(x=df_filtered['Orders'], y=df_filtered['Predicted_Gap'], mode='markers', marker=dict(size=df_filtered['Risk_Score']*10, color=df_filtered['Risk_Score'], colorscale=[[0,'#10b981'],[0.5,'#f59e0b'],[1,'#dc2626']], showscale=True, colorbar=dict(title="Risk")), text=df_filtered['Year'], hovertemplate='<b>Year %{text}</b><br>Orders: %{x}<br>Gap: %{y}<extra></extra>'), row=1, col=1)
    fig2.add_trace(go.Bar(x=df_filtered['Year'], y=df_filtered['Risk_Score'], marker_color=[{'Low':'#10b981','Medium':'#f59e0b','High':'#dc2626'}[lvl] for lvl in df_filtered['Risk_Level']], text=df_filtered['Risk_Level'], textposition='outside'), row=1, col=2)
    fig2.update_layout(height=400, showlegend=False, template='plotly_white')
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

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
