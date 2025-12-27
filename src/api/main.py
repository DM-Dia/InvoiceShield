from fastapi import FastAPI, UploadFile, File
from src.ocr.ocr_extractor import extract_text
from src.parser.invoice_parser import parse_invoice
from src.rules.rule_engine import rule_flags
from src.db.database import SessionLocal, engine
from src.db.models import Base
from src.db.crud import save_invoice

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/upload-invoice")
async def upload_invoice(file: UploadFile = File(...)):
    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_text(path)
    parsed = parse_invoice(text)
    parsed["anomaly"] = rule_flags(parsed)

    db = SessionLocal()
    saved = save_invoice(db, parsed)

    return {"invoice_id": saved.id, "details": parsed}

@app.get("/")
def health_check():
    return {
        "status": "ok",
        "service": "InvoiceShield API",
        "version": "1.0.0"
    }