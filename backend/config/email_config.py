import smtplib
from email.mime.text import MIMEText

sender = "pemmaanupriya225@gmail.com"
receiver = "gogulaavinash20@gmail.com"
password = "mmsk yhfj asws ptlv"   # Gmail App Password

print("creating email content")

# create the email content
message = MIMEText("Sending email using Python")
message["Subject"] = "Test email from python"
message["From"] = sender
message["To"] = receiver

print("connecting to gmail smtp server....")
server = smtplib.SMTP("smtp.gmail.com", 587)

print("starting tls encryption...")
server.starttls()

print("logging in...")
server.login(sender, password)

print("sending email..")
server.sendmail(sender, receiver, message.as_string())

print("email sent successfully!...")

print("closing server connection...")
server.quit()

print("program finished")
