# Automate Updates to Catalog Information

This project is based on the final lab from the **Google IT Automation with Python** course.

## Project overview

The goal of this lab is to automate the process of updating an online fruit store catalog using supplier data.

The supplier provides:

- large `.tiff` fruit images
- `.txt` files with fruit descriptions

The automation workflow processes this data, uploads it to a web server, generates a PDF report, sends it by email, and checks system health.

## Files in this project

### Main scripts

- `changeImage.py`  
  Converts supplier `.tiff` images into `.jpeg`, resizes them to `600x400`, and converts them to RGB.

- `supplier_image_upload.py`  
  Uploads processed `.jpeg` images to the fruit catalog web server.

- `run.py`  
  Reads supplier description files, builds JSON objects, and uploads fruit data to the Django web application.

- `report_email.py`  
  Reads supplier description files again, creates a formatted PDF summary report, and sends it by email.

- `health_check.py`  
  Checks CPU, disk space, memory, and localhost resolution, then sends an alert email if a problem is detected.

### Helper modules

- `reports.py`  
  Provides the `generate_report()` function used to build the PDF report.

- `emails.py`  
  Provides helper functions for creating and sending emails, including emails with PDF attachments and alert emails without attachments.

## Execution order

1. `changeImage.py` — process supplier images
2. `supplier_image_upload.py` — upload processed images to the server
3. `run.py` — upload fruit descriptions and metadata to the catalog
4. `report_email.py` — generate the PDF report and send it by email
5. `health_check.py` — check system health and send alert emails if needed

## Skills practiced

This lab combines multiple topics:

- image processing with Pillow
- file handling
- HTTP requests with `requests`
- JSON data handling
- uploading files to a web server
- PDF generation with ReportLab
- sending emails with attachments
- basic system monitoring with `psutil`, `shutil`, and `socket`

## Notes

This project was completed as a learning exercise and portfolio example while studying Python automation, Linux, cloud fundamentals, and IAM-related technical skills.

## Course

Google IT Automation with Python