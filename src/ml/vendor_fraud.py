import pandas as pd

def fraud_score(vendor_data, items):
    score = 0
    
    # Price volatility
    std = items["unit_price"].std()
    mean = items["unit_price"].mean()
    volatility = (std / mean) if mean else 0
    score += min(35, volatility * 100)

    # Duplicate invoice numbers
    duplicates = vendor_data["invoice_number"].duplicated().sum()
    score += min(25, duplicates * 10)

    # High tax % frequency
    high_tax = vendor_data[vendor_data["tax_percent"] > 30]
    score += min(20, len(high_tax) * 5)

    # Anomaly density
    flagged = vendor_data[vendor_data["anomaly"] != "No Issues"]
    density = len(flagged) / len(vendor_data)
    score += min(20, density * 100)

    return round(score, 2)
