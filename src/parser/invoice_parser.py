import re
from datetime import datetime

def extract_vendor(text):
    for line in text:
        if "vendor" in line.lower():
            return line.split(":")[-1].strip()
    return "Unknown Vendor"

def extract_invoice_number(text):
    for line in text:
        if "invoice" in line.lower():
            cleaned = re.sub(r"[^A-Za-z0-9]", "", line)
            return cleaned
    return "NA"

def extract_date(text):
    for line in text:
        try:
            return str(datetime.strptime(line.strip(), "%d/%m/%Y").date())
        except:
            continue
    return None

def extract_tax(text):
    for line in text:
        if "%" in line:
            try:
                return float(re.findall(r"(\d+)", line)[0])
            except:
                pass
    return 0.0

def parse_invoice(text_blocks):
    return {
        "vendor": extract_vendor(text_blocks),
        "invoice_number": extract_invoice_number(text_blocks),
        "invoice_date": extract_date(text_blocks),
        "tax_percent": extract_tax(text_blocks),
        "raw_text": " ".join(text_blocks)
    }