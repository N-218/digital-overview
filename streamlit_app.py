import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# 1. PAGE CONFIGURATION & SETUP
# =========================
st.set_page_config(
    page_title="Boeing Digital Oversight Dashboard",
    layout="wide",
    page_icon="✈️"
)

# Define Corporate Color Palette
NAVY_BLUE = "#00315a"  # Boeing primary color (Dark Navy)
LIGHT_BLUE = "#4a90e2" # Accent/Highlight Blue
MEDIUM_BLUE = "#2196F3" # Chart line color
RED_RISK = "#E74C3C"   # High Risk
YELLOW_RISK = "#F39C12" # Medium Risk
GREEN_RISK = "#2ECC71"  # Low Risk

# =========================
# 2. CUSTOM STYLE (Professional Card Theme)
# =========================
st.markdown(f"""
<style>
/* Main App Styling */
.stApp {{
    background-color: #f0f2f6; /* Very subtle light grey background */
    font-family: 'Inter', sans-serif;
}}
h1, h2, h3, .st-b5 {{
    color: {NAVY_BLUE};
    font-weight: 700;
}}
/* Separator */
hr {{
    border: 0;
    height: 1px;
    background-image: linear-gradient(to right, rgba(0, 0, 0, 0), rgba(0, 49, 90, 0.3), rgba(0, 0, 0, 0));
    margin: 1.5rem 0;
}}
/* Metric Styling for Cards */
[data-testid="stMetric"] {{
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 20px 20px 10px 20px;
    box-shadow: 0 4px 12px rgba(0, 49, 90, 0.08); /* Subtle Navy shadow */
    border-left: 5px solid {LIGHT_BLUE}; /* Blue accent border */
}}
/* Metric Value (Large Number) */
[data-testid="stMetricValue"] {{
    font-size: 2.2rem !important;
    color: {NAVY_BLUE} !important;
}}
/* Sidebar Styling */
.sidebar .sidebar-content {{
    background-color: #FFFFFF;
    border-right: 1px solid #e0e0e0;
}}
/* Expander Card Style */
[data-testid="stExpander"] div[role="button"] {{
    background-color: #FFFFFF;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 49, 90, 0.05);
}}
</style>
""", unsafe_allow_html=True)


# =========================
# 3. MOCK DATA & DATA LOADING
# =========================

# Updated Mock Data based on the user's provided CSV structure
MOCK_DATA = {
    'Year': [2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028],
    'PlannedOutput': [264, 372, 456, 456, 456, 0, 0, 0],
    'ActualOutput': [263, 387, 396, 265, 455, 0, 0, 0],
    'Orders': [395, 626, 1075, 2364, 5848, 0, 0, 0],
    'Backlog': [341, 365, 433, 303, 164, 0, 0, 0],
    'ProductionGap': [410, 30, 260, 191, 110, 0, 0, 0],
    'Backlog_Change_Pct': [-459.2, -150.07, 0.186, -0.007, 0.119, 0, 0, 0],
    'NetLoss': [-227.3, -546.0, -633.0, -476.9, -724.3, 0, 0, 0],
    'ForwardLosses': [-206.7, 0, 0, -217.0, -585.0, 0, 0, 0],
    # Imputing 0 for missing ExcessCapacityCost values in early years to ensure data structure integrity
    'ExcessCapacityCost': [0, 0, 0, -70, -55, 0, 0, 0], 
    'Risk_Level': ['Low', 'Low', 'Medium', 'Medium', 'High', 'High', 'High', 'High'],
    'Predicted_Gap': [-75.6, 27.0, 129.6, 232.2, 334.8, 437.4, 540.0, 642.6]
}

def load_data(uploaded_file):
    """Loads uploaded data or uses mock data."""
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            # Ensure critical columns are present even if the user uploads a file
            required_cols = ['Year', 'ProductionGap', 'Risk_Level', 'Predicted_Gap', 'Orders']
            if not all(col in df.columns for col in required_cols):
                 st.error(f"Uploaded CSV is missing one or more required columns: {', '.join(required_cols)}")
                 st.stop()
        except Exception as e:
            st.error(f"Error reading uploaded file: {e}")
            df = pd.DataFrame(MOCK_DATA)
            st.info("Reverted to **Mock Data** due to file error.")
    else:
        # Use mock data if no file is uploaded
        df = pd.DataFrame(MOCK_DATA)
        st.info("Using **Mock Data** for demonstration. Please upload your CSV file in the sidebar to use real data.")

    # Convert Risk Level to Numeric Score
    risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
    df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

    return df

# =========================
# 4. SIDEBAR (Upload & Filters)
# =========================
st.sidebar.title("✈️ Boeing Oversight")
uploaded_file = st.sidebar.file_uploader("Upload Digital_Oversight_Forecast.csv", type=["csv"])

df = load_data(uploaded_file)

# Sidebar Filters
st.sidebar.header("🔍 Filter Scope")
# Ensure min/max operations work even if the data range is small
min_year = int(df["Year"].min()) if not df.empty else 2021
max_year = int(df["Year"].max()) if not df.empty else 2028
default_range = (min_year, max_year)
if min_year == max_year:
    default_range = (min_year, max_year) # Handle single year case
else:
    default_range = (min_year, max_year)

year_range = st.sidebar.slider(
    "Select Year Range",
    min_year,
    max_year,
    default_range
)
risk_levels = st.sidebar.multiselect(
    "Select Risk Levels",
    df["Risk_Level"].unique(),
    default=df["Risk_Level"].unique()
)

# Apply Filters
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]

if df_filtered.empty:
    st.error("No data matches the selected filters. Please adjust the range or risk levels.")
    st.stop()


# =========================
# 5. HEADER & KPI METRICS (Card Layout)
# =========================
st.markdown(f"""
<div style='text-align:left; padding: 10px 0;'>
    <h1 style='color:{NAVY_BLUE}; margin-bottom: 0px;'>Digital Oversight Dashboard</h1>
    <p style='color:#6c757d; font-size:18px;'>Strategic Forecast, Risk Assessment, and Implementation Roadmap</p>
</div>
<hr>
""", unsafe_allow_html=True)

st.markdown("### 📈 Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

# Calculate KPI values (handle potential NaN/empty sums)
total_predicted_gap = df_filtered['Predicted_Gap'].sum()
max_risk_score = df_filtered['Risk_Score'].max()
max_risk_year = df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year'] if not df_filtered.empty and df_filtered['Risk_Score'].max() == 3 else 'N/A'
total_orders = df_filtered['Orders'].sum()

col1.metric("Total Predicted Gap (Units)", f"{total_predicted_gap:,.0f}")
col2.metric("Max Oversight Risk Score", f"{max_risk_score}")
col3.metric("Year of Peak Risk", f"{max_risk_year}")
col4.metric("Total Confirmed Orders", f"{total_orders:,}")

st.markdown("---")

# =========================
# 6. FORECAST + RISK VISUALS
# =========================
st.markdown("### 📊 Production Forecast and Risk Analysis")

# Use a container for a clean, contained visual section
with st.container():
    st.markdown("""
        <div style='background-color: #FFFFFF; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 49, 90, 0.05);'>
        <h4 style='color: #00315a; margin-top: 0;'>Gap Forecast & Annual Risk Breakdown</h4>
    """, unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        # Line Chart: Production Gap Forecast
        fig1 = px.line(
            df_filtered,
            x="Year",
            y=["ProductionGap", "Predicted_Gap"],
            markers=True,
            labels={"value": "Aircraft Gap (Units)", "variable": "Gap Type"},
            title="Production Gap Forecast Trend",
            color_discrete_sequence=[MEDIUM_BLUE, NAVY_BLUE]
        )
        fig1.update_layout(
            title_x=0.5,
            template="plotly_white",
            height=400,
            margin=dict(l=40, r=20, t=50, b=40),
            legend_title_text=''
        )
        st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})

    with col_chart2:
        # Bar Chart: Risk Levels by Year
        fig2 = px.bar(
            df_filtered,
            x="Year",
            y="Risk_Score",
            color="Risk_Level",
            text="Risk_Level",
            title="Annual Supplier Oversight Risk Level",
            color_discrete_map={"Low": GREEN_RISK, "Medium": YELLOW_RISK, "High": RED_RISK}
        )
        fig2.update_layout(
            title_x=0.5,
            template="plotly_white",
            height=400,
            margin=dict(l=40, r=20, t=50, b=40),
            yaxis_title="Risk Score (1-3)",
        )
        fig2.update_traces(textposition='outside')
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

# =========================
# 7. ROADMAP (Implementation Timeline)
# =========================
st.markdown("### 🗺️ Digital Oversight Implementation Roadmap (2025)")

phases = pd.DataFrame([
    dict(Phase='01 - Planning & Vendor Setup', Start='2025-01-01', Finish='2025-02-28', Category='Phase I: Foundation'),
    dict(Phase='02 - Telemetry Installation', Start='2025-03-01', Finish='2025-04-30', Category='Phase II: Data Acquisition'),
    dict(Phase='03 - Supplier Integration', Start='2025-05-01', Finish='2025-06-30', Category='Phase II: Data Acquisition'),
    dict(Phase='04 - Pilot & Analytics Engine', Start='2025-07-01', Finish='2025-10-31', Category='Phase III: Intelligence'),
    dict(Phase='05 - Dashboard Deployment', Start='2025-11-01', Finish='2025-12-15', Category='Phase IV: Delivery'),
    dict(Phase('06 - Review & Scale Decision', Start='2025-12-16', Finish='2025-12-31', Category='Phase IV: Delivery')
])
phases["Start"] = pd.to_datetime(phases["Start"])
phases["Finish"] = pd.to_datetime(phases["Finish"])

timeline_colors = {
    'Phase I: Foundation': LIGHT_BLUE,
    'Phase II: Data Acquisition': MEDIUM_BLUE,
    'Phase III: Intelligence': YELLOW_RISK,
    'Phase IV: Delivery': NAVY_BLUE,
}

fig3 = px.timeline(
    phases,
    x_start="Start",
    x_end="Finish",
    y="Phase",
    color="Category",
    color_discrete_map=timeline_colors,
    title="Project Execution Timeline: 2025",
)
fig3.update_yaxes(autorange="reversed")
fig3.update_layout(
    height=450,
    title_x=0.5,
    title_font=dict(size=18, color=NAVY_BLUE),
    margin=dict(l=60, r=60, t=60, b=60),
    template="plotly_white",
    hoverlabel=dict(bgcolor="white", font_size=14, font_family="sans-serif")
)
st.plotly_chart(fig3, use_container_width=True)


# =========================
# 8. RECOMMENDATIONS & ACTION ITEMS
# =========================
st.markdown("### 💡 Strategic Summary & Action Items")
st.markdown("""
<div style='background-color: #FFFFFF; padding: 25px; border-radius: 12px; border-left: 5px solid #F39C12; box-shadow: 0 4px 12px rgba(0, 49, 90, 0.05);'>
    <h5 style='color: #00315a; margin-top: 0;'>Key Takeaways from the Forecast:</h5>
    <ul>
        <li><b>Mitigation Focus:</b> The highest risk exposure aligns with the largest Predicted Gaps (e.g., in {max_risk_year}). Resource allocation should prioritize oversight in this window.</li>
        <li><b>Technology Integration:</b> Accelerate <b>Phase II (Data Acquisition)</b> to establish digital telemetry and supplier integration, which is critical for moving from reactive oversight to predictive risk management.</li>
        <li><b>Intelligence Layer:</b> Dedicate sufficient resources to <b>Phase III (Intelligence)</b> to ensure the analytics engine provides actionable insights, not just raw data.</li>
    </ul>
</div>
""".format(max_risk_year=max_risk_year), unsafe_allow_html=True)


# =========================
# 9. FOOTER
# =========================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:12px; color:#6c757d;'>&copy; 2025 The Boeing Company | Digital Oversight Pilot | All rights reserved. | App Version 1.1</p>", unsafe_allow_html=True)
