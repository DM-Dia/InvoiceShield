from .models import Invoice

def save_invoice(db, data):
    obj = Invoice(
        vendor=data["vendor"],
        invoice_number=data["invoice_number"],
        invoice_date=data["invoice_date"],
        tax_percent=data["tax_percent"],
        anomaly=data["anomaly"]
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
