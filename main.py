import time
import os

from backend.config.dask_config import start_dask
from backend.processing.pipeline import build_pipeline
from backend.anomaly.detector import detect_anomalies
from backend.config.email_config import send_anomaly_email

ADMIN_EMAIL = "admin@example.com"


def main():
    client = start_dask()
    print(client)
    print(f"Dashboard link: {client.dashboard_link}")
    print("\n" + "=" * 50)

    start = time.time()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    LOG_FILE = os.path.join(
        BASE_DIR, "backend", "log_generator", "realtime_logs.csv"
    )

    # Build pipeline
    log_df = build_pipeline(LOG_FILE)

    total_logs = log_df.count().compute()
    end = time.time()

    print("Total logs parsed:", total_logs)
    print("Time taken:", round(end - start, 2), "seconds")

    print("\nRunning anomaly detection...")

    anomalies = detect_anomalies(log_df)

    if anomalies.empty:
        print("No anomalies detected")
    else:
        print(f"🚨 {len(anomalies)} anomalies detected!")

        for _, row in anomalies.iterrows():
            anomaly_data = {
                "timestamp": row["timestamp"],
                "error_count": row["error_count"],
                "z_score": row["z_score"],
            }

            send_anomaly_email(ADMIN_EMAIL, anomaly_data)

            print(
                f"📧 Alert sent | Time: {row['timestamp']} | "
                f"Errors: {row['error_count']}"
            )

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
