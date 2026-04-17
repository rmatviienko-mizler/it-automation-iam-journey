#!/usr/bin/env python3

import os
import datetime
import reports
import emails

path = os.path.expanduser("~/supplier-data/descriptions/")
pdf_path = "/tmp/processed.pdf"

today = datetime.date.today().strftime("%B %d, %Y")
title = "Processed Update on " + today

summary = ""

for filename in os.listdir(path):
    if filename.lower().endswith(".txt"):
        file_path = os.path.join(path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        if len(lines) < 2:
            continue

        name = lines[0]
        weight = lines[1]

        summary += f"name: {name}<br/>weight: {weight}<br/><br/>"

if __name__ == "__main__":
    reports.generate_report(pdf_path, title, summary)

    sender = "automation@example.com"
    receiver = "student@example.com"
    subject = "Upload Completed - Online Fruit Store"
    body = "All fruits are uploaded to our website successfully. A detailed list is attached to this email."

    message = emails.generate_email(sender, receiver, subject, body, pdf_path)
    emails.send_email(message)