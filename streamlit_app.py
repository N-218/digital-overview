import streamlit as st

import pandas as pd

import plotly.express as px
 
# ========= PAGE CONFIGURATION =============

st.set_page_config(

    page_title="Boeing Digital Oversight Dashboard",

    layout="wide",

    page_icon="✈️"

)
 
# ========= PROFESSIONAL STYLING ===========

st.markdown("""
<style>

    .stApp {

        background: linear-gradient(135deg, #f5fafd 0%, #dde6ef 100%);

    }

    .stApp::before {

        content: "";

        background-image: url("https://upload.wikimedia.org/wikipedia/commons/3/36/Boeing_full_logo.svg");

        background-size: 320px;

        background-repeat: no-repeat;

        background-position: top right;

        opacity: 0.08;

        position: fixed;

        top: 28px; right: 60px; bottom: 0; left: 0;

        z-index: 0;

        pointer-events: none;

    }

    .kpi-card {

        background: #ffffff88;

        border-radius: 15px;

        box-shadow: 0 2px 12px 0 #99b4cd44;

        padding: 25px 16px 18px 16px;

        margin-bottom: 8px;

        text-align: center;

    }

    h1, h3, h4 {

        color: #144e95 !important;

        font-family: "Segoe UI", Arial, sans-serif;

        margin-bottom: 4px;

    }

    .kpi-label {

        font-size: 16px;

        color: #587bac;

        font-weight: 600;

    }

    .footer {

        color: #6586ad;

        font-size: 13px;

        margin-top: 36px;

        padding-bottom: 6px;

    }
</style>

""", unsafe_allow_html=True)
 
# ======= SIDEBAR UPLOAD & FILTERS =========

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/3/36/Boeing_full_logo.svg", width=200)

st.sidebar.markdown("---")

st.sidebar.title("Upload & Filters")

uploaded_file = st.sidebar.file_uploader("Upload your Digital_Oversight_Forecast.csv", type=["csv"])

if uploaded_file:

    df = pd.read_csv(uploaded_file)

else:

    st.markdown(

        "<div style='padding:100px; text-align:center'>"

        "<h2 style='color:#165291;'>Waiting for Data...</h2>"

        "<p style='color:#3d5d77;'>Upload your CSV in the sidebar to view the dashboard.</p>"

        "</div>", unsafe_allow_html=True

    )

    st.stop()
 
risk_mapping = {"Low": 1, "Medium": 2, "High": 3}

df["Risk_Score"] = df["Risk_Level"].map(risk_mapping)
 
st.sidebar.header("Filters")

year_range = st.sidebar.slider(

    "Select Year Range",

    int(df["Year"].min()), int(df["Year"].max()),

    (int(df["Year"].min()), int(df["Year"].max()))

)

risk_levels = st.sidebar.multiselect(

    "Select Risk Levels",

    df["Risk_Level"].unique(), default=df["Risk_Level"].unique()

)

df_filtered = df[

    (df["Year"] >= year_range[0]) & (df["Year"] <= year_range[1])
& (df["Risk_Level"].isin(risk_levels))

]
 
# ========= HEADER =========================

st.markdown("""
<div style='text-align: center;'>
<h1 style='font-size:39px; letter-spacing:1.5px; font-weight:700; text-shadow: 0 3px 15px #a9bdcd22;'>

    ✈️ Boeing Digital Oversight Dashboard
</h1>
<p style='font-size:17px; color: #5570a2; margin-bottom:10px;'>Forecast | Risk | Roadmap | Strategic Recommendations</p>
<hr style='width:48%; border:1.2px solid #b4c7dc;'>
</div>

""", unsafe_allow_html=True)
 
# ========= KPI METRICS ====================

st.markdown("### Key Metrics")

metrics = [

    {

        "label": "Predicted Gap",

        "value": f"{df_filtered['Predicted_Gap'].sum():,.0f}",

        "desc": "Total units forecasted below planned capacity"

    },

    {

        "label": "Max Risk Score",

        "value": f"{df_filtered['Risk_Score'].max()}",

        "desc": "Highest risk score in selected period"

    },

    {

        "label": "High-Risk Year",

        "value": f"{df_filtered.loc[df_filtered['Risk_Score'].idxmax(), 'Year']}",

        "desc": "Year with greatest oversight risk"

    },

    {

        "label": "Total Orders",

        "value": f"{df_filtered['Orders'].sum():,}",

        "desc": "Sum of all orders in this period"

    }

]

kpi_cols = st.columns(4)

for col, metric in zip(kpi_cols, metrics):

    with col:

        st.markdown(f"<div class='kpi-card'>"

                    f"<div class='kpi-label'>{metric['label']}</div>"

                    f"<div style='font-size:2.0em; font-weight:700; color:#144e95;'>{metric['value']}</div>"

                    f"<div style='font-size:13px; color:#7faaca;'>{metric['desc']}</div>"

                    "</div>", unsafe_allow_html=True)
 
# ======= CHARTS SECTION ===================

st.markdown("### Forecast & Risk Charts")

viz_cols = st.columns(2)
 
with viz_cols[0]:

    st.subheader("Production Gap Forecast")

    fig1 = px.line(

        df_filtered, x="Year",

        y=["ProductionGap", "Predicted_Gap"],

        markers=True,

        labels={"value": "Gap", "variable": "Gap Type"},

        color_discrete_sequence=["#165291", "#e97824"]

    )

    fig1.update_layout(

        height=350, template="plotly_white", title_x=0.5,

        legend=dict(title="", orientation="h", x=0.13, y=-0.33),

        plot_bgcolor="#f3f6fa"

    )

    st.plotly_chart(fig1, use_container_width=True)
 
with viz_cols[1]:

    st.subheader("Oversight Risk by Year")

    fig2 = px.bar(

        df_filtered,

        x="Year", y="Risk_Score", color="Risk_Level", text="Risk_Score",

        color_discrete_map={"Low": "#27ae60", "Medium": "#FDDB2F", "High": "#E75E2B"}

    )

    fig2.update_layout(

        height=350, template="plotly_white", title_x=0.5,

        showlegend=True, plot_bgcolor="#f3f6fa"

    )

    st.plotly_chart(fig2, use_container_width=True)
 
# ====== ROADMAP GANTT CHART ===============

st.markdown("### Implementation Roadmap")

phases = pd.DataFrame([

    dict(Phase='Planning & Vendor Setup', Start='2025-01-01', Finish='2025-02-28', Category='Planning'),

    dict(Phase='Telemetry Installation', Start='2025-03-01', Finish='2025-04-30', Category='Implementation'),

    dict(Phase='Supplier Integration', Start='2025-05-01', Finish='2025-06-30', Category='Integration'),

    dict(Phase='Pilot & Analytics', Start='2025-07-01', Finish='2025-12-31', Category='Analytics'),

    dict(Phase='Dashboard Deployment', Start='2025-07-01', Finish='2025-12-31', Category='Dashboard'),

    dict(Phase='Review & Scale Decision', Start='2025-12-31', Finish='2025-12-31', Category='Review')

])

phases["Start"] = pd.to_datetime(phases["Start"])

phases["Finish"] = pd.to_datetime(phases["Finish"])

colors = {

    'Planning': '#1080d0', 'Implementation': '#2ECC71', 'Integration': '#9B59B6',

    'Analytics': '#FDB842', 'Dashboard': '#28B2B6', 'Review': '#E74C3C'

}

fig3 = px.timeline(

    phases, x_start="Start", x_end="Finish",

    y="Phase", color="Category", color_discrete_map=colors,

    category_orders={"Phase": list(phases["Phase"])}

)

fig3.update_yaxes(autorange="reversed")

fig3.update_layout(height=290, title_x=0.5, template="plotly_white", margin=dict(l=10, r=10, t=32, b=10))

st.plotly_chart(fig3, use_container_width=True)
 
# ========== RECOMMENDATIONS ===============

st.markdown("### 💡 Executive Recommendations")

with st.expander("Recommended Actions:"):

    high_gap_years = df_filtered[df_filtered["Predicted_Gap"] > df_filtered["Predicted_Gap"].quantile(0.75)]["Year"].tolist()

    high_risk_years = df_filtered[df_filtered["Risk_Level"] == "High"]["Year"].tolist()

    st.markdown(f"""

    - <b>🔺 Oversight focus needed in:</b> <span style='color:#E74C3C'>{', '.join(map(str, high_risk_years))}</span> (high risk) 

    - <b>🚦 Major gaps in:</b> <span style='color:#F39C12'>{', '.join(map(str, high_gap_years))}</span> (capacity shortfall)

    - <b>📈 Integrate digital telemetry</b> for predictive monitoring & intervention.

    - <b>🛎️ Automate</b> alerts for supplier exceptions.

    - <b>📊 Prioritize analytics</b> during Integration & Analytics roadmap phases.

    """, unsafe_allow_html=True)
 
# ============ FOOTER ======================

st.markdown('<hr>', unsafe_allow_html=True)

st.markdown(

    "<div class='footer'><p style='text-align:center;'>"

    "© 2025 Boeing | Digital Oversight Pilot | Professional Board Dashboard"

    "</p></div>", unsafe_allow_html=True

)

 
