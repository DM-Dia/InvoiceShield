import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sqlalchemy import create_engine, text

# -----------------------------
# App Config
# -----------------------------
st.set_page_config(
    page_title="InvoiceShield Dashboard",
    layout="wide"
)

# -----------------------------
# Paths & Database
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "invoices.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

# -----------------------------
# Title
# -----------------------------
st.title("📄 InvoiceShield – Invoice Risk & Fraud Dashboard")

menu = st.sidebar.radio(
    "Navigation",
    ["Invoices Overview", "Analytics", "Upload Invoice"]
)

# =====================================================
# 📊 1. INVOICES OVERVIEW
# =====================================================
if menu == "Invoices Overview":
    st.subheader("Processed Invoices")

    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM invoices"), conn)

    if df.empty:
        st.info("No invoices processed yet.")
    else:
        st.dataframe(df, use_container_width=True)

# =====================================================
# 📈 2. ANALYTICS
# =====================================================
if menu == "Analytics":
    st.subheader("Invoice Analytics")

    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM invoices"), conn)

    if df.empty:
        st.warning("No data available for analytics.")
    else:
        col1, col2 = st.columns(2)

        # -----------------------------
        # Vendor Spend Chart
        # -----------------------------
        with col1:
            st.markdown("### 💰 Vendor-wise Total Spend")
            vendor_spend = df.groupby("vendor")["amount"].sum()

            fig, ax = plt.subplots()
            vendor_spend.plot(kind="bar", ax=ax)
            ax.set_ylabel("Amount")
            ax.set_xlabel("Vendor")
            ax.set_title("Total Spend per Vendor")
            st.pyplot(fig)

        # -----------------------------
        # Anomaly Rate Chart
        # -----------------------------
        with col2:
            st.markdown("### 🚨 Anomaly Rate")
            anomaly_counts = df["anomaly"].value_counts()

            fig, ax = plt.subplots()
            anomaly_counts.plot(
                kind="pie",
                autopct="%1.1f%%",
                ax=ax,
                startangle=90
            )
            ax.set_ylabel("")
            ax.set_title("Anomalous vs Normal Invoices")
            st.pyplot(fig)

# =====================================================
# 📤 3. UPLOAD & PROCESS INVOICE
# =====================================================
if menu == "Upload Invoice":
    st.subheader("Upload a New Invoice")

    file = st.file_uploader(
        "Upload invoice file",
        type=["pdf", "png", "jpg", "jpeg"]
    )

    if file:
        temp_path = BASE_DIR / f"temp_{file.name}"

        with open(temp_path, "wb") as f:
            f.write(file.read())

        st.info("Processing invoice...")

        # -----------------------------
        # Correct absolute imports
        # -----------------------------
        from src.ocr.ocr_extractor import extract_text
        from src.parser.invoice_parser import parse_invoice
        from src.rules.rule_engine import rule_flags
        from src.fraud.fraud_score import calculate_fraud_score
        from src.reports.pdf_report import generate_invoice_report
        from src.db.crud import save_invoice
        from src.db.database import SessionLocal

        # -----------------------------
        # OCR + Parsing
        # -----------------------------
        extracted_text = extract_text(str(temp_path))
        parsed = parse_invoice(extracted_text)

        # -----------------------------
        # Rule-based anomaly
        # -----------------------------
        rules_result = rule_flags(parsed)
        parsed["rules"] = rules_result
        parsed["anomaly"] = any(rules_result.values())

        # -----------------------------
        # Fraud score
        # -----------------------------
        fraud_score = calculate_fraud_score(
            parsed["anomaly"],
            rules_result
        )
        parsed["fraud_score"] = fraud_score

        # -----------------------------
        # Save to DB
        # -----------------------------
        db = SessionLocal()
        save_invoice(db, parsed)
        db.close()

        # -----------------------------
        # Generate PDF Report
        # -----------------------------
        report_path = BASE_DIR / f"invoice_report_{parsed['invoice_id']}.pdf"
        generate_invoice_report(parsed, str(report_path))

        # -----------------------------
        # UI Output
        # -----------------------------
        st.success("Invoice processed successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📋 Parsed Invoice Data")
            st.json(parsed)

        with col2:
            st.markdown("### 🔍 Extracted Text")
            st.text_area(
                "OCR Output",
                "\n".join(extracted_text),
                height=300
            )

        # -----------------------------
        # PDF Download
        # -----------------------------
        with open(report_path, "rb") as f:
            st.download_button(
                label="📄 Download Invoice Report (PDF)",
                data=f,
                file_name=report_path.name,
                mime="application/pdf"
            )
