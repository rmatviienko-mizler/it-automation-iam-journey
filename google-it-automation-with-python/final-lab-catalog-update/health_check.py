#!/usr/bin/env python3

import shutil
import psutil
import socket
import emails

sender = "automation@example.com"
receiver = "student@example.com"
body = "Please check your system and resolve the issue as soon as possible."


def send_alert(subject):
    message = emails.generate_alert_email(sender, receiver, subject, body)
    emails.send_email(message)


disk = shutil.disk_usage("/")
free_disk_percent = disk.free / disk.total * 100

if free_disk_percent < 20:
    send_alert("Error - Available disk space is less than 20%")


cpu_percent = psutil.cpu_percent(1)

if cpu_percent > 80:
    send_alert("Error - CPU usage is over 80%")


memory = psutil.virtual_memory()
min_memory = 100 * 1024 * 1024  # 100 MB in bytes

if memory.available < min_memory:
    send_alert("Error - Available memory is less than 100MB")

try:
    localhost_ip = socket.gethostbyname("localhost")
    if localhost_ip != "127.0.0.1":
        send_alert("Error - localhost cannot be resolved to 127.0.0.1")
except socket.gaierror:
    send_alert("Error - localhost cannot be resolved to 127.0.0.1")