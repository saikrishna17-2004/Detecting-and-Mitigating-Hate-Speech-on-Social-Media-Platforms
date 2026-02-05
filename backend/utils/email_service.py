"""
Email Service for sending warning and suspension notifications
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from typing import Optional

class EmailService:
    """Service for sending email notifications"""
    
    def __init__(self):
        # Email configuration from environment variables
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        self.sender_password = os.getenv('SENDER_PASSWORD', '')
        self.enabled = bool(self.sender_email and self.sender_password)
        
        if not self.enabled:
            print("WARNING: Email service not configured. Set SMTP credentials in .env file")
    
    def send_email(self, recipient_email: str, subject: str, body_html: str) -> bool:
        """Send an email"""
        if not self.enabled:
            print(f"[EMAIL DISABLED] Would send to {recipient_email}: {subject}")
            return False
        
        try:
            # Create message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.sender_email
            message['To'] = recipient_email
            
            # Add HTML body
            html_part = MIMEText(body_html, 'html')
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            print(f"SUCCESS: Email sent to {recipient_email}: {subject}")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to send email to {recipient_email}: {e}")
            return False
    
    def send_warning_email(self, user_email: str, username: str, warning_count: int, 
                          max_warnings: int, violation_content: str, category: str) -> bool:
        """Send warning notification email"""
        subject = f"⚠️ Community Guidelines Warning - Strike {warning_count}/{max_warnings}"
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #ff9800; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ background-color: #fff3cd; padding: 20px; margin: 20px 0; border-left: 4px solid #ff9800; }}
                .violation {{ background-color: #f5f5f5; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                .footer {{ color: #666; font-size: 12px; margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; }}
                .warning-count {{ font-size: 24px; font-weight: bold; color: #ff5722; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Community Guidelines Warning</h1>
                </div>
                
                <div class="content">
                    <p>Dear <strong>{username}</strong>,</p>
                    
                    <p>We have detected content that violates our community guidelines.</p>
                    
                    <div class="warning-count">
                        Warning {warning_count} of {max_warnings}
                    </div>
                    
                    <div class="violation">
                        <p><strong>Violation Type:</strong> {category.title()}</p>
                        <p><strong>Content:</strong></p>
                        <p style="font-style: italic; color: #666;">"{violation_content[:200]}{'...' if len(violation_content) > 200 else ''}"</p>
                        <p><strong>Time:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                    </div>
                    
                    <p><strong>What this means:</strong></p>
                    <ul>
                        <li>Your content has been flagged and may be removed</li>
                        <li>This is warning {warning_count} of {max_warnings}</li>
                        <li>{'⚠️ <strong>You are approaching suspension</strong>' if warning_count >= max_warnings - 1 else 'Please review our community guidelines'}</li>
                        <li>{'⛔ <strong>One more violation will result in account suspension</strong>' if warning_count >= max_warnings - 1 else 'Future violations may result in account suspension'}</li>
                    </ul>
                    
                    <p><strong>What you should do:</strong></p>
                    <ul>
                        <li>Review our community guidelines</li>
                        <li>Be mindful of the content you post</li>
                        <li>Treat all community members with respect</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p>This is an automated message from the Hate Speech Detection & Moderation System.</p>
                    <p>If you believe this is an error, please contact our support team.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, body_html)
    
    def send_suspension_email(self, user_email: str, username: str, 
                            violation_count: int, final_violation_content: str,
                            category: str) -> bool:
        """Send account suspension notification email"""
        subject = "⛔ Account Suspended - Community Guidelines Violation"
        
        body_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #d32f2f; color: white; padding: 20px; text-align: center; border-radius: 5px; }}
                .content {{ background-color: #ffebee; padding: 20px; margin: 20px 0; border-left: 4px solid #d32f2f; }}
                .violation {{ background-color: #f5f5f5; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                .footer {{ color: #666; font-size: 12px; margin-top: 20px; padding-top: 20px; border-top: 1px solid #ddd; }}
                .suspended {{ font-size: 28px; font-weight: bold; color: #d32f2f; text-align: center; padding: 15px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⛔ Account Suspended</h1>
                </div>
                
                <div class="content">
                    <p>Dear <strong>{username}</strong>,</p>
                    
                    <div class="suspended">
                        YOUR ACCOUNT HAS BEEN SUSPENDED
                    </div>
                    
                    <p>After {violation_count} violations of our community guidelines, your account has been suspended.</p>
                    
                    <div class="violation">
                        <p><strong>Final Violation Type:</strong> {category.title()}</p>
                        <p><strong>Content:</strong></p>
                        <p style="font-style: italic; color: #666;">"{final_violation_content[:200]}{'...' if len(final_violation_content) > 200 else ''}"</p>
                        <p><strong>Suspension Time:</strong> {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
                        <p><strong>Total Violations:</strong> {violation_count}</p>
                    </div>
                    
                    <p><strong>What this means:</strong></p>
                    <ul>
                        <li>❌ You can no longer post content</li>
                        <li>❌ Your account is temporarily suspended</li>
                        <li>❌ Your existing content may be hidden or removed</li>
                        <li>❌ You cannot interact with other users</li>
                    </ul>
                    
                    <p><strong>Why this happened:</strong></p>
                    <ul>
                        <li>You received multiple warnings about violating community guidelines</li>
                        <li>You continued to post content that violates our policies</li>
                        <li>Our platform has zero tolerance for hate speech and harassment</li>
                    </ul>
                    
                    <p><strong>What you can do:</strong></p>
                    <ul>
                        <li>Review our community guidelines thoroughly</li>
                        <li>Contact support if you believe this is an error</li>
                        <li>Appeal the suspension through our support channel</li>
                    </ul>
                </div>
                
                <div class="footer">
                    <p>This is an automated message from the Hate Speech Detection & Moderation System.</p>
                    <p>For appeals or questions, contact: support@example.com</p>
                    <p><strong>We are committed to maintaining a safe and respectful community for all users.</strong></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return self.send_email(user_email, subject, body_html)
    
    def send_test_email(self, recipient_email: str) -> bool:
        """Send a test email to verify configuration"""
        subject = "✅ Email Service Test"
        
        body_html = """
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>✅ Email Service is Working!</h2>
            <p>This is a test email from the Hate Speech Detection & Moderation System.</p>
            <p>If you received this, your email configuration is correct.</p>
            <p><strong>Time:</strong> """ + datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') + """ UTC</p>
        </body>
        </html>
        """
        
        return self.send_email(recipient_email, subject, body_html)


# Singleton instance
email_service = EmailService()
