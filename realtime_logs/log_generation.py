import os
import time
import random
import csv
from datetime import datetime

#  Always anchor to project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_FILE = os.path.join(DATA_DIR, "realtime_logs.csv")

os.makedirs(DATA_DIR, exist_ok=True)

services = ["auth", "payment", "orders", "search"]
info_msgs = ["Request OK", "User login", "Cache hit"]
error_msgs = ["DB failure", "Timeout", "Null pointer"]

# Write header once
with open(LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["timestamp", "level", "service", "message"])

print("Real-time log producer started...")

while True:
    level = random.choices(
        ["INFO", "WARN", "ERROR"],
        weights=[0.7, 0.1, 0.2],
    )[0]

    row = [
        datetime.now().isoformat(),
        level,
        random.choice(services),
        random.choice(error_msgs if level == "ERROR" else info_msgs),
    ]

    with open(LOG_FILE, "a", newline="") as f:
        csv.writer(f).writerow(row)

    time.sleep(0.3)