# emailing.py

import smtplib
from email.message import EmailMessage
import json
import os
from cryptography.fernet import Fernet

class Emailing:
    def __init__(self, config_path, key_path):
        self.config = self.load_config(config_path)
        self.fernet_key = self.load_key(key_path)
        self.smtp_server = self.config['smtp_server']
        self.smtp_port = self.config['smtp_port']
        self.sender_email = self.decrypt(self.config['email'])
        self.smtp_password = self.decrypt(self.config['password'])

    def load_key(self, key_path):
        with open(key_path, 'rb') as key_file:
            return key_file.read()

    def decrypt(self, encrypted_data):
        fernet = Fernet(self.fernet_key)
        return fernet.decrypt(encrypted_data.encode()).decode()

    def load_config(self, config_path):
        with open(config_path) as config_file:
            return json.load(config_file)

    def create_email(self, recipient_emails, subject, body, attachment_path=None):
        message = EmailMessage()
        message['From'] = self.sender_email
        message['To'] = ", ".join(recipient_emails)
        message['Subject'] = subject
        message.set_content(body)
        
        if attachment_path:
            with open(attachment_path, 'rb') as attachment:
                message.add_attachment(
                    attachment.read(),
                    maintype='application',
                    subtype='octet-stream',
                    filename=os.path.basename(attachment_path)
                )
        return message

    def send_email(self, message):
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.smtp_password)
            server.send_message(message)
