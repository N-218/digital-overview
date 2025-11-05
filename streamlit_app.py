uploaded_file = st.sidebar.file_uploader("Upload Digital_Oversight_Forecast.csv", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    st.warning("Please upload your CSV in the sidebar to see the dashboard.")
    st.stop()

