import streamlit as st
import plotly.express as px

from processing.pipeline import build_pipeline
from anomaly.detector import detect_anomalies

st.title("Python Based High Throughput Log Analytics Monitoring Engine")

# Build log dataframe
log_df = build_pipeline("data/sample_log.log")

# Detect anomalies (Dask → Pandas)
anomaly_df = detect_anomalies(log_df).compute()

st.subheader("Anomalies Detected in Logs")

# Plot anomaly score
if not anomaly_df.empty:
    fig = px.line(
        anomaly_df,
        x='timestamp',
        y='anomaly_score',
        title='Anomaly Scores Over Time'
    )
    st.plotly_chart(fig)
else:
    st.warning("No anomalies detected.")

st.subheader("Anomalous Log Entries")
st.dataframe(anomaly_df)

# Threshold filter
threshold = st.slider(
    "Anomaly Score Threshold",
    min_value=0.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)

filtered_anomalies = anomaly_df[
    anomaly_df['anomaly_score'].abs() >= threshold
]

st.subheader("Filtered Anomalies")
st.dataframe(filtered_anomalies)
