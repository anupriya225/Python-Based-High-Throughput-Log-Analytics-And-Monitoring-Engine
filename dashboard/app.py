import streamlit as st
import plotly.express as px
import os
import sys
import pandas as pd

# ---------------- PATH SETUP ----------------
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_path not in sys.path:
    sys.path.insert(0, root_path)

# ---------------- IMPORT BACKEND MODULES ----------------
try:
    from backend.processing.pipeline import build_pipeline
    from backend.anomaly.detector import detect_anomalies
except ImportError as e:
    st.error(f"Import Error: {e}")
    st.stop()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Log Analytics Engine", layout="wide")

st.title("Python Based High Throughput Log Analytics Monitoring Engine")

# ---------------- SIDEBAR ----------------
st.sidebar.header("Settings")

uploaded_file = st.sidebar.file_uploader(
    "Upload Log CSV File",
    type=["csv"]
)

if st.sidebar.button("Refresh Dashboard"):
    st.rerun()

# ---------------- MAIN LOGIC ----------------
if uploaded_file is None:
    st.info("👈 Please upload a log CSV file to view the dashboard.")
    st.stop()

try:
    # Build processing pipeline
    log_df_dask = build_pipeline(uploaded_file)

    # Convert to pandas
    log_data = log_df_dask.compute()

    # Detect anomalies
    result = detect_anomalies(log_df_dask)
    anomaly_df = result.compute() if hasattr(result, "compute") else result

    # ---------------- VISUALIZATIONS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Log Level Distribution")

        if not log_data.empty:
            level_counts = log_data["level"].value_counts().reset_index()
            level_counts.columns = ["level", "count"]

            fig_pie = px.pie(
                level_counts,
                values="count",
                names="level",
                title="Distribution of Log Levels"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("No log data available.")

    with col2:
        st.subheader("Log Levels Over Time")

        if not log_data.empty:
            fig_time = px.line(
                log_data.sort_values("timestamp"),
                x="timestamp",
                y="level",
                title="Log Level Timeline"
            )
            st.plotly_chart(fig_time, use_container_width=True)

    # ---------------- STATUS & ALERTS ----------------
    st.divider()

    total_logs = len(log_data)
    error_logs_count = len(log_data[log_data["level"] == "ERROR"])
    error_percentage = (error_logs_count / total_logs) * 100 if total_logs > 0 else 0

    if not anomaly_df.empty or error_percentage > 90:
        st.error("🚨 ALERT: Critical Issues Detected!")
        if error_percentage > 90:
            st.warning(f"High error rate detected: {error_percentage:.2f}%")
    else:
        st.success("✅ System Stable: No anomalies detected")

    # ---------------- RAW DATA ----------------
    if st.checkbox("Show raw processed log data"):
        st.dataframe(log_data.tail(20), use_container_width=True)

except Exception as e:
    st.error(f"Unexpected error occurred: {e}")
