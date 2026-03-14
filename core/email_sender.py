# 🐉 LUO GATE — EMAIL SYSTEM
import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_LOGIN = "a4935b001@smtp-brevo.com"
SMTP_KEY = os.getenv("BREVO_SMTP_KEY")
FROM_EMAIL = os.getenv("BREVO_EMAIL")

def send_email(to, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = FROM_EMAIL
        msg["To"] = to
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_LOGIN, SMTP_KEY)
            server.send_message(msg)
        print(f"📧 Email sent to {to}!")
        return True
    except Exception as e:
        print(f"⚠️ Email failed: {e}")
        return False

print("📧 Email System loaded!")
