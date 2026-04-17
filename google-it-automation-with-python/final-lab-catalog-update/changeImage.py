#!/usr/bin/env python3

from PIL import Image
import os

path = os.path.expanduser("~/supplier-data/images/")

for image in os.listdir(path):
    if image.lower().endswith(".tiff"):
        input_path = os.path.join(path, image)
        name, _ = os.path.splitext(image)
        new_name = name + ".jpeg"
        output_path = os.path.join(path, new_name)

        with Image.open(input_path) as img:
            converted = img.convert("RGB")
            resized = converted.resize((600, 400))
            resized.save(output_path, format="JPEG")