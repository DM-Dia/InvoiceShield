from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_invoice_report(invoice: dict, output_path: str):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica", 12)
    c.drawString(50, y, "InvoiceShield – Invoice Report")

    y -= 30
    for key, value in invoice.items():
        c.drawString(50, y, f"{key}: {value}")
        y -= 20

        if y < 50:
            c.showPage()
            y = height - 50

    c.save()