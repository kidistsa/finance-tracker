import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class EmailService:
    
    def __init__(self):
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.email_user = getattr(settings, 'EMAIL_USER', '')
        self.email_password = getattr(settings, 'EMAIL_PASSWORD', '')
        self.app_url = getattr(settings, 'APP_URL', 'http://localhost:5173')
    
    def send_email(self, to_email, subject, html_content):
        if not self.email_user or not self.email_password:
            print('Email not configured')
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.email_user
            msg['To'] = to_email
            msg.attach(MIMEText(html_content, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f'Email error: {e}')
            return False
    
    def send_verification_email(self, email, token):
        link = f'{self.app_url}/verify-email?token={token}'
        html = f'''
        <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto;">
            <h2 style="color: #d64daf;">Verify Your Email</h2>
            <p>Click the button below to verify your email address:</p>
            <a href="{link}" style="display: inline-block; background: #d64daf; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a>
            <p>Or copy this link: {link}</p>
            <p>This link expires in 24 hours.</p>
        </div>
        '''
        return self.send_email(email, 'Verify Your Email - Birr Finance', html)
    
    def send_reset_email(self, email, token):
        link = f'{self.app_url}/reset-password?token={token}'
        html = f'''
        <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto;">
            <h2 style="color: #d64daf;">Reset Your Password</h2>
            <p>Click the button below to reset your password:</p>
            <a href="{link}" style="display: inline-block; background: #d64daf; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a>
            <p>This link expires in 1 hour.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </div>
        '''
        return self.send_email(email, 'Reset Your Password - Birr Finance', html)
