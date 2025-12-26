from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_invoice_report(data, path="invoice_report.pdf"):
    c = canvas.Canvas(path, pagesize=letter)
    y = 750

    c.setFont("Helvetica-Bold", 18)
    c.drawString(30, y, "InvoiceShield Report")
    y -= 50

    c.setFont("Helvetica", 12)
    for key, val in data.items():
        c.drawString(30, y, f"{key}: {val}")
        y -= 20

    c.save()
    return path