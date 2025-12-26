from fastapi import FastAPI, UploadFile, File
from ocr.ocr_extractor import extract_text
from parser.invoice_parser import parse_invoice
from rules.rule_engine import rule_flags
from db.database import SessionLocal, engine
from db.models import Base
from db.crud import save_invoice

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