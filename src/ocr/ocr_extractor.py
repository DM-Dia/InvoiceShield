import easyocr
from pdf2image import convert_from_path
import os

reader = easyocr.Reader(['en'])

def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    img_paths = []
    for i, img in enumerate(images):
        img_path = f"{pdf_path}_page_{i}.png"
        img.save(img_path, 'PNG')
        img_paths.append(img_path)
    return img_paths

def extract_text(path):
    if path.endswith(".pdf"):
        images = pdf_to_images(path)
        text_blocks = []
        for img in images:
            text_blocks.extend(reader.readtext(img, detail=0))
        return text_blocks
    else:
        return reader.readtext(path, detail=0)