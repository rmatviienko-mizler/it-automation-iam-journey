#!/usr/bin/env python3

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_report(pdf_path, title, body):
    report = SimpleDocTemplate(pdf_path)
    styles = getSampleStyleSheet()
    
    report_title = Paragraph(title, styles["h1"])
    report_body = Paragraph(body, styles["BodyText"])
    spacer = Spacer(1, 20)
    
    report.build([report_title, spacer, report_body])