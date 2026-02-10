import pandas as pd
import dask.dataframe as dd


def detect_anomalies(log_df):
    # Convert Dask DF → Pandas DF safely
    pdf = log_df.compute()

    # Ensure datetime
    pdf["timestamp"] = pd.to_datetime(pdf["timestamp"])

    # Set index
    pdf = pdf.set_index("timestamp")

    # Resample per minute
    agg_df = (
        pdf
        .resample("1T")
        .size()
        .to_frame(name="error_count")
    )

    # Z-score anomaly detection
    mean = agg_df["error_count"].mean()
    std = agg_df["error_count"].std()

    if std == 0 or pd.isna(std):
        agg_df["z_score"] = 0
    else:
        agg_df["z_score"] = (agg_df["error_count"] - mean) / std

    anomalies = agg_df[agg_df["z_score"].abs() > 3]

    anomalies = anomalies.reset_index()

    return anomalies
