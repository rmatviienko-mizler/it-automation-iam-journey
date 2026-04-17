#!/usr/bin/env python3

import email.message
import mimetypes
import smtplib
import os

def generate_email(sender, recipient, subject, body, attachment_path):
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    attachment_filename = os.path.basename(attachment_path)
    mime_type, _ = mimetypes.guess_type(attachment_path)
    maintype, subtype = mime_type.split("/")

    with open(attachment_path, "rb") as f:
        message.add_attachment(f.read(), maintype=maintype, subtype=subtype, filename=attachment_filename)

    return message

def generate_alert_email(sender, recipient, subject, body):
    message = email.message.EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    return message

def send_email(message):
    mail_server = smtplib.SMTP('localhost')
    mail_server.send_message(message)
    mail_server.quit()