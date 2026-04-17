#!/usr/bin/env python3

import os
import requests

url = "http://localhost/upload/"
path = os.path.expanduser("~/supplier-data/images/")

for f in os.listdir(path):
    if f.lower().endswith(".jpeg"):
        file_path = os.path.join(path, f)
        with open(file_path, "rb") as opened:
            response = requests.post(url, files={"file": opened})
            response.raise_for_status()