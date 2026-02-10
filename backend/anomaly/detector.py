# anomaly/detector.py

import dask.dataframe as dd

def detect_anomalies(log_df, z_threshold=3):

    # Ensure timestamp is datetime
    log_df['timestamp'] = dd.to_datetime(log_df['timestamp'])

    # Filter ERROR logs
    error_logs = log_df[log_df['level'] == 'ERROR']

    # Count errors per minute
    error_counts = (
        error_logs
        .set_index('timestamp')
        .resample('1T')
        .size()
        .rename('error_count')
        .reset_index()
    )

    # Compute mean & std
    mean = error_counts['error_count'].mean().compute()
    std = error_counts['error_count'].std().compute()

    # Z-score anomaly score
    if std == 0:
        error_counts['anomaly_score'] = 0
    else:
        error_counts['anomaly_score'] = (error_counts['error_count'] - mean) / std

    # Mark anomalies
    error_counts['is_anomaly'] = error_counts['anomaly_score'].abs() > z_threshold

    return error_counts[error_counts['is_anomaly']]
