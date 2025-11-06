import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# Page Configuration
# =========================
st.set_page_config(page_title="Digital Oversight Dashboard", layout="wide")

# =========================
# Background and Boeing Logo
# =========================
st.markdown(
    """
    <style>
    /* Gradient background */
    .stApp {
        background: linear-gradient(to bottom right, #f5f6fa, #ffffff);
    }
    /* Boeing logo watermark */
    .stApp::before {
        content: "";
        background-image: url("https://upload.wikimedia.org/wikipedia/commons/3/36/Boeing_full_logo.svg");
        background-size: 20%;
        background-repeat: no-repeat;
        background-position: top right;
        opacity: 0.1;
        position: fixed;
        top: 0;
        right: 0;
        bottom: 0;
        left: 0;
        z-index: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# Sidebar: Upload & Filters
# =========================
st.sidebar.title("Upload Your Data")
uploaded_file = st.sidebar.file_uploader("Upload Digital_Oversight_Forecast.csv", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload your CSV in the sidebar to see the dashboard.")
    st.stop()

# Map risk levels to numeric scores
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}
df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)

# Sidebar Filters
st.sidebar.header("Filters")
year_range = st.sidebar.slider(
    "Select Year Range", int(df["Year"].min()), int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)
risk_levels = st.sidebar.multiselect(
    "Select Risk Level(s)", options=df["Risk_Level"].unique(), default=df["Risk_Level"].unique()
)

# Apply filters
df_filtered = df[(df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])]
df_filtered = df_filtered[df_filtered["Risk_Level"].isin(risk_levels)]

# =========================
# Professional Dashboard Title
# =========================
st.markdown("""
<div style='text-align: center;'>
    <h1 style='font-size:40px; color:#0a3d62; margin-bottom:0px;'>Digital Oversight Dashboard</h1>
    <p style='font-size:18px; color:#34495e; margin-top:0px;'>Forecast & Risk Overview</p>
    <hr style='border:1px solid #dcdde1; width:50%; margin:auto'>
</div>
""", unsafe_allow_html=True)

# =========================
# KPI Highlights (Top Row)
# =========================
st.markdown("### 🚩 Key Metrics")
col1, col2, col3, col4 = st.columns([1,1,1,1])

col1.metric("Total Predicted Gap", f"{df_filtered['Predicted_Gap'].sum():.1f}")
col2.metric("Max Risk Score", f"{df_filtered['Risk_Score'].max()}")
col3.metric("Year with Highest Risk", f"{df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']}")
col4.metric("Total Orders", f"{df_filtered['Orders'].sum()}")

st.markdown("---")

# =========================
# Charts Section (Middle Row)
# =========================
st.markdown("### 📊 Forecast & Risk Charts")
col1, col2 = st.columns([1,1])  # Side-by-side charts for compactness

with col1:
    st.subheader("Forecast Gap Over Time")
    fig1 = px.line(
        df_filtered,
        x="Year",
        y="Predicted_Gap",
        markers=True,
        color="Risk_Level",
        hover_data=["PlannedOutput", "ActualOutput", "Backlog"],
        title="Forecasted Gap by Year"
    )
    fig1.update_layout(title_x=0.5, template="plotly_white", margin=dict(l=10,r=10,t=30,b=10))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Risk Levels")
    fig2 = px.bar(
        df_filtered,
        x="Year",
        y="Risk_Score",
        color="Risk_Level",
        text="Risk_Score",
        title="Risk Scores by Year"
    )
    fig2.update_layout(title_x=0.5, template="plotly_white", margin=dict(l=10,r=10,t=30,b=10))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# =========================
# Recommendations Section (Bottom Row)
# =========================
st.markdown("### ✅ Recommendations")
with st.expander("Click to view actionable insights"):
    high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > 300]["Year"].tolist()
    if high_gap_years:
        st.markdown(f"- ⚠️ High predicted gaps detected in {', '.join(map(str, high_gap_years))} — prioritize supplier oversight.")
    else:
        st.markdown("- ✅ Predicted gaps are within manageable range.")

    st.markdown(
        "- Integrate digital telemetry for predictive monitoring.\n"
        "- Add automated alerts for suppliers exceeding risk thresholds.\n"
        "- Focus on years with high Risk Score for proactive intervention."
    )
