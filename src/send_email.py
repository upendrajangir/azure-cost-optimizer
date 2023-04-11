import os
import smtplib
from email.message import EmailMessage
from typing import List
from smtplib import SMTPException


def read_template(template_file: str, msg: str) -> str:
    with open(template_file, "r") as file:
        template = file.read()
    return template.replace("{message}", msg)


def send_email(
    subject: str,
    msg: str,
    from_email: str,
    to_email: List[str],
    template_file: str = None,
    is_html: bool = False,
) -> None:
    # Read SMTP configuration from environment variables
    smtp_server = os.environ.get("SMTP_SERVER", "smtp.example.com")
    smtp_port = int(os.environ.get("SMTP_PORT", 587))
    smtp_username = os.environ.get("SMTP_USERNAME", "your_username")
    smtp_password = os.environ.get("SMTP_PASSWORD", "your_password")

    # Read the email template
    if template_file:
        msg = read_template(template_file, msg)

    # Create the email message
    email_msg = EmailMessage()
    if is_html:
        email_msg.add_alternative(msg, subtype="html")
    else:
        email_msg.set_content(msg)
    email_msg["Subject"] = subject
    email_msg["From"] = from_email
    email_msg["To"] = ", ".join(to_email)

    # Send the email using the SMTP server
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(email_msg)
            print(f"Email sent to {', '.join(to_email)}")
    except SMTPException as e:
        print(f"SMTP error: {e}")
    except Exception as e:
        print(f"Error sending email: {e}")
