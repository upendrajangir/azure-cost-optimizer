import smtplib
import logging

# Set logger
logger = logging.getLogger(__name__)


def send_email(
    email: str,
    password: str,
    recipient: str,
    subject: str,
    body: str,
    host: str = "smtp.gmail.com",
    port: int = 587,
) -> bool:
    """Send email using SMTP server (default == Gmail).

    Args:
        email (str): Email address.
        password (str): Password.
        recipient (str): Email address of recipient.
        subject (str): Subject of email.
        body (str): Body of email.

    Returns:
        bool: True if email was sent successfully, False otherwise.
    """
    try:
        # Create SMTP session
        session = smtplib.SMTP(host, port)

        # Start TLS for security
        session.starttls()

        # Authentication
        session.login(email, password)

        # Compose message
        message = f"Subject: {subject}\n\n{body}"

        # Send email
        session.sendmail(email, recipient, message)

        # Terminate session
        session.quit()

        # Log success
        logger.info(f"Email sent successfully to {recipient}")

        return True
    except Exception as err:
        # Log error
        logger.error(f"Email failed to send: {err}")

        return False
