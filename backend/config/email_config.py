import smtplib
from email.mime.text import MIMEText

SENDER = "pemmaanupriya225@gmail.com"
PASSWORD = "mmsk yhfj asws ptlv"   # Gmail App Password


def send_anomaly_email(to_email, anomaly):
    subject = "🚨 Log Anomaly Detected"
    body = f"""
An anomaly has been detected in the log system.

Timestamp   : {anomaly['timestamp']}
Error Count : {anomaly['error_count']}
Z-Score     : {anomaly['z_score']}
"""

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = SENDER
    message["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER, PASSWORD)
    server.sendmail(SENDER, to_email, message.as_string())
    server.quit()
