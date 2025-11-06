import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Boeing Executive Dashboard",
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
                    box-shadow: 0 4px 20px rgba(0, 48, 135, 0.15); }

.dashboard-title { color: white; font-size: 2.5rem; font-weight: 700; margin: 0; }
.dashboard-subtitle { color: #a8c5e8; font-size: 1.1rem; margin-top: 0.5rem; }

.logo-space { text-align: right; color: white; font-weight: 600; font-size: 1.5rem; letter-spacing: 2px; }

.section-header { color: #003087; font-size: 1.5rem; font-weight: 600; margin: 2rem 0 1rem 0; padding-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0; }

.alert-box { padding: 1rem 1.5rem; border-radius: 8px; margin: 1rem 0; }
.alert-box.critical { background: #fee2e2; border-left: 4px solid #dc2626; }
.alert-box.success { background: #d1fae5; border-left: 4px solid #10b981; }
</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR: FILE UPLOAD & FILTERS
# =========================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 2rem 0;'>
        <h2 style='color: white; margin: 0; font-size: 1.8rem; letter-spacing: 3px;'>BOEING</h2>
        <p style='color: #94a3b8; font-size: 0.75rem; margin-top: 0.25rem;'>Executive Digital Oversight</p>
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
    year_range = st.slider("Year Range", int(df["Year"].min()), int(df["Year"].max()), (int(df["Year"].min()), int(df["Year"].max())))
    risk_levels = st.multiselect("Risk Levels", df["Risk_Level"].unique(), default=df["Risk_Level"].unique())
    if "Supplier" in df.columns:
        suppliers = st.multiselect("Suppliers", df["Supplier"].unique(), default=df["Supplier"].unique())
    adjust_factor = st.slider("Predicted Gap Adjustment (%)", -50, 50, 0)
    metrics_options = st.multiselect(
        "Select Metrics to Display",
        ["Total Predicted Gap", "High-Risk Periods", "Critical Year", "Total Orders"],
        default=["Total Predicted Gap", "High-Risk Periods", "Critical Year", "Total Orders"]
    )

# Apply filters
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]
if "Supplier" in df.columns:
    df_filtered = df_filtered[df_filtered["Supplier"].isin(suppliers)]
df_filtered["Adjusted_Gap"] = df_filtered["Predicted_Gap"] * (1 + adjust_factor / 100)

# =========================
# HEADER
# =========================
st.markdown(f"""
<div class='dashboard-header'>
    <div style='display: flex; justify-content: space-between; align-items: center;'>
        <div>
            <h1 class='dashboard-title'>Boeing Executive Dashboard</h1>
            <p class='dashboard-subtitle'>Supply Chain Intelligence & Risk Management System</p>
        </div>
        <div class='logo-space'>✈️</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# METRICS
# =========================
col1, col2, col3, col4 = st.columns(4)
total_gap = df_filtered['Predicted_Gap'].sum()
total_orders = df_filtered['Orders'].sum()
avg_orders = df_filtered['Orders'].mean()
high_risk_count = len(df_filtered[df_filtered['Risk_Level'] == 'High'])
critical_year_row = df_filtered.loc[df_filtered['Risk_Score'].idxmax()]

if "Total Predicted Gap" in metrics_options:
    col1.metric("Total Predicted Gap", f"{total_gap:,.0f}", delta=f"{(total_gap/total_orders*100):.1f}% of orders")
if "High-Risk Periods" in metrics_options:
    col2.metric("High-Risk Periods", high_risk_count, delta=f"{(high_risk_count/len(df_filtered)*100):.0f}% of timeline")
if "Critical Year" in metrics_options:
    col3.metric("Critical Year", critical_year_row['Year'], delta=f"Gap: {critical_year_row['Predicted_Gap']:,}")
if "Total Orders" in metrics_options:
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
# TABS FOR INTERACTIVE DASHBOARD
# =========================
tab1, tab2, tab3 = st.tabs(["Overview", "Production Analysis", "Supplier Risk"])

# -------------------------
# OVERVIEW TAB
# -------------------------
with tab1:
    st.markdown("<h2 class='section-header'>📈 Summary Metrics</h2>", unsafe_allow_html=True)
    st.write("Use sidebar to adjust year range, risk levels, suppliers, and gap adjustments.")

# -------------------------
# PRODUCTION ANALYSIS TAB
# -------------------------
with tab2:
    st.markdown("<h2 class='section-header'>📊 Production Gap Analysis</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3,2])

    with col1:
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=df_filtered['Year'], y=df_filtered['ProductionGap'], 
            name='Actual Gap', mode='lines+markers', 
            line=dict(color='#94a3b8', width=3), marker=dict(size=8)
        ))
        fig1.add_trace(go.Scatter(
            x=df_filtered['Year'], y=df_filtered['Adjusted_Gap'], 
            name='Adjusted Gap', mode='lines+markers', 
            line=dict(color='#003087', width=4), marker=dict(size=10, symbol='diamond')
        ))
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

# -------------------------
# SUPPLIER RISK TAB
# -------------------------
with tab3:
    st.markdown("<h2 class='section-header'>📊 Orders vs Gap Correlation</h2>", unsafe_allow_html=True)
    fig2 = make_subplots(rows=1, cols=2, subplot_titles=('Orders vs Predicted Gap', 'Year-over-Year Risk Progression'), specs=[[{"secondary_y": False}, {"type": "bar"}]])

    fig2.add_trace(go.Scatter(
        x=df_filtered['Orders'], y=df_filtered['Adjusted_Gap'], mode='markers',
        marker=dict(size=df_filtered['Risk_Score']*10, color=df_filtered['Risk_Score'],
                    colorscale=[[0, '#10b981'], [0.5, '#f59e0b'], [1, '#dc2626']], showscale=True),
        text=df_filtered['Year'], hovertemplate='<b>Year %{text}</b><br>Orders: %{x}<br>Gap: %{y}<extra></extra>',
        name='Year Data'), row=1, col=1
    )

    colors_map = {'Low': '#10b981', 'Medium': '#f59e0b', 'High': '#dc2626'}
    fig2.add_trace(go.Bar(
        x=df_filtered['Year'], y=df_filtered['Risk_Score'], 
        marker_color=[colors_map[l] for l in df_filtered['Risk_Level']], 
        text=df_filtered['Risk_Level'], textposition='outside', name='Risk Level'
    ), row=1, col=2)

    fig2.update_layout(height=400, showlegend=False, template='plotly_white', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

# =========================
# DATA TABLE WITH DOWNLOAD
# =========================
with st.expander("📊 View Detailed Data Table"):
    st.dataframe(df_filtered.style.background_gradient(subset=['Risk_Score'], cmap='RdYlGn_r'), use_container_width=True, height=400)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=df_filtered.to_csv(index=False),
        file_name="filtered_forecast.csv",
        mime="text/csv"
    )

# =========================
# FOOTER
# =========================
st.markdown("""
<div style='text-align:center; padding:2rem 0 1rem 0; border-top:2px solid #e2e8f0;'>
    <p style='color:#64748b; font-size:0.875rem; margin:0;'><strong>Boeing Digital Oversight System</strong> | Version 2.0 | © 2025 The Boeing Company</p>
    <p style='color:#94a3b8; font-size:0.75rem; margin-top:0.5rem;'>Powered by Advanced Analytics & Machine Learning | Last Updated: November 2025</p>
</div>
""", unsafe_allow_html=True)

