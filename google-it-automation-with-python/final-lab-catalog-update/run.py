#!/usr/bin/env python3

import os
import requests

url = "http://34.70.155.110/fruits/"
path = os.path.expanduser("~/supplier-data/descriptions/")

for filename in os.listdir(path):
    if filename.lower().endswith(".txt"):
        file_path = os.path.join(path, filename)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        if len(lines) < 3:
            continue

        name = lines[0]
        weight = int(lines[1].split()[0])
        description = " ".join(lines[2:])

        base_name, _ = os.path.splitext(filename)
        image_name = base_name + ".jpeg"

        fruit = {
            "name": name,
            "weight": weight,
            "description": description,
            "image_name": image_name
        }

        response = requests.post(url, json=fruit)
        response.raise_for_status()