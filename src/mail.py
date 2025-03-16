from pathlib import Path
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Email details


def send_html_mail(sender_email: str, sender_password: str, receiver_email: str, subject: str, html_fpath: str | Path):

    # Load your HTML content
    with open(html_fpath, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    # Send the email
    with smtplib.SMTP("smtp.mail.com", 465) as server: #587, 465  # Replace with your SMTP server
        server.starttls()
        server.login(sender_email, sender_password)  # Use app passwords or environment variables for security
        server.sendmail(sender_email, receiver_email, msg.as_string())

    print("Email sent successfully!")