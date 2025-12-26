import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# -----------------------------
# Database setup (safe path)
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "invoices.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

# -----------------------------
# UI
# -----------------------------
st.title("InvoiceShield Dashboard")

menu = st.sidebar.radio("Menu", ["Invoices", "Upload Invoice"])

# -----------------------------
# View invoices
# -----------------------------
if menu == "Invoices":
    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM invoices"), conn)

    st.subheader("Processed Invoices")
    st.dataframe(df)

# -----------------------------
# Upload invoice
# -----------------------------
if menu == "Upload Invoice":
    file = st.file_uploader("Upload invoice", type=["pdf", "png", "jpg"])

    if file:
        temp_path = BASE_DIR / f"temp_{file.name}"

        with open(temp_path, "wb") as f:
            f.write(file.read())

        # Correct absolute imports
        from src.ocr.ocr_extractor import extract_text
        from src.parser.invoice_parser import parse_invoice
        from src.rules.rule_engine import rule_flags
        from src.db.crud import save_invoice
        from src.db.database import SessionLocal

        extracted_text = extract_text(str(temp_path))
        parsed = parse_invoice(extracted_text)
        parsed["anomaly"] = rule_flags(parsed)

        db = SessionLocal()
        save_invoice(db, parsed)
        db.close()

        st.success("Invoice processed successfully!")
        st.json(parsed)
        st.text_area("Extracted Text", "\n".join(extracted_text), height=300)