"""Email notification provider implementation."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .base import BaseNotificationProvider


class EmailProvider(BaseNotificationProvider):
    """Email notification provider using SMTP."""

    def _send_notification(self, message: str) -> None:
        """Send notification message via Email.
        
        Args:
            message: The message string to send
        
        Raises:
            Exception: If notification fails
        """
        try:
            subject = self.config['subject']
            smtp_server = self.config['smtp_server']
            smtp_port = self.config['smtp_port']
            username = self.config['username']
            password = self.config['password']
            from_email = self.config['from_email']
            to_email = self.config['to_email']
            
            # Create email message
            msg = MIMEMultipart()
            msg['From'] = from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add message body
            msg.attach(MIMEText(message, 'plain'))
            
            # Send email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  # Enable TLS encryption
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP error: {e}")
        except Exception as e:
            raise Exception(f"Failed to send email notification: {e}")
