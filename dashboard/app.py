import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from sqlalchemy import create_engine, text

# ------------------------------------
# App configuration
# ------------------------------------
st.set_page_config(
    page_title="InvoiceShield Dashboard",
    layout="wide"
)

# ------------------------------------
# Paths & database
# ------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "invoices.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

# ------------------------------------
# Title & navigation
# ------------------------------------
st.title(" InvoiceShield – Invoice Risk & Fraud Dashboard")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Invoices Overview",
        "Analytics",
        "Vendor Clustering",
        "Upload Invoice"
    ]
)

# =====================================================
# 1️⃣ INVOICES OVERVIEW
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
# 2️⃣ ANALYTICS (Spend + Anomaly Rate)
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
        # Vendor Spend
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
        # Anomaly Rate
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
# 3️⃣ VENDOR CLUSTERING (DBSCAN)
# =====================================================
if menu == "Vendor Clustering":
    st.subheader("Vendor Behavioral Clustering")

    with engine.connect() as conn:
        df = pd.read_sql(text("SELECT * FROM invoices"), conn)

    if df.empty:
        st.warning("Not enough data for vendor clustering.")
    else:
        from src.fraud.vendor_clustering import cluster_vendors

        vendor_clusters = cluster_vendors(df)

        st.markdown("### 🧩 Vendor Clusters (DBSCAN)")
        st.dataframe(vendor_clusters, use_container_width=True)

        outliers = vendor_clusters[vendor_clusters["cluster"] == -1]

        if not outliers.empty:
            st.warning("⚠️ Potential risky vendors detected (outliers)")
            st.dataframe(outliers, use_container_width=True)
        else:
            st.success("No abnormal vendor behavior detected.")

# =====================================================
# 4️⃣ UPLOAD & PROCESS INVOICE
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

        # ------------------------------------
        # Imports
        # ------------------------------------
        from src.ocr.ocr_extractor import extract_text
        from src.parser.invoice_parser import parse_invoice
        from src.rules.rule_engine import rule_flags
        from src.fraud.fraud_score import calculate_fraud_score
        from src.fraud.fraud_explanation import explain_fraud_score
        from src.reports.pdf_report import generate_invoice_report
        from src.db.crud import save_invoice
        from src.db.database import SessionLocal

        # ------------------------------------
        # OCR + parsing
        # ------------------------------------
        extracted_text = extract_text(str(temp_path))
        parsed = parse_invoice(extracted_text)

        # ------------------------------------
        # Rules & anomaly
        # ------------------------------------
        rules_result = rule_flags(parsed)
        parsed["rules"] = rules_result
        parsed["anomaly"] = any(rules_result.values())

        # ------------------------------------
        # Fraud score
        # ------------------------------------
        fraud_score = calculate_fraud_score(
            parsed["anomaly"],
            rules_result
        )
        parsed["fraud_score"] = fraud_score

        # ------------------------------------
        # Fraud explanation
        # ------------------------------------
        explanation = explain_fraud_score(
            parsed["anomaly"],
            rules_result,
            fraud_score
        )

        # ------------------------------------
        # Save to DB
        # ------------------------------------
        db = SessionLocal()
        saved_invoice = save_invoice(db, parsed)
        db.close()

        parsed["invoice_id"] = saved_invoice.id

        # ------------------------------------
        # Generate PDF report
        # ------------------------------------
        report_path = BASE_DIR / f"invoice_report_{parsed['invoice_id']}.pdf"
        generate_invoice_report(parsed, str(report_path))

        # ------------------------------------
        # UI output
        # ------------------------------------
        st.success("Invoice processed successfully!")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📋 Parsed Invoice Data")
            st.json(parsed)

            st.markdown("### 🧠 Fraud Risk Explanation")
            st.json(explanation)

        with col2:
            st.markdown("### 🔍 Extracted Text")
            st.text_area(
                "OCR Output",
                "\n".join(extracted_text),
                height=300
            )

        # ------------------------------------
        # PDF download
        # ------------------------------------
        with open(report_path, "rb") as f:
            st.download_button(
                label="📄 Download Invoice Report (PDF)",
                data=f,
                file_name=report_path.name,
                mime="application/pdf"
            )
