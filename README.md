# 📄 InvoiceShield

**Invoice Anomaly Detection & Vendor Fraud Analysis System**

InvoiceShield is an end-to-end system for **processing invoices, detecting anomalies, and analyzing vendor risk** using OCR, rule-based logic, and machine learning.
It provides a usable dashboard for analytics, fraud scoring, and audit-ready reporting.

---

## ✨ Key Features

* Invoice upload (PDF / PNG / JPG)
* OCR-based text extraction (EasyOCR)
* Rule-based + ML anomaly detection
* Vendor behavior clustering (DBSCAN)
* Fraud risk scoring with explanations
* Interactive Streamlit dashboard
* Downloadable PDF invoice reports
* FastAPI backend with Swagger UI


## Approach

* **OCR** converts invoices into structured text
* **Rules + ML models** flag anomalous invoices
* **DBSCAN clustering** groups vendors by behavior and identifies outliers
* **Fraud score (0–100)** summarizes invoice risk with explainable reasons
* Results are stored and visualized through a dashboard

## Project Structure

```text
InvoiceShield/
├── src/
│   ├── api/
│   │   └── main.py
│   ├── ocr/
│   ├── parser/
│   ├── rules/
│   ├── fraud/
│   ├── reports/
│   └── db/
├── dashboard/
│   └── app.py
├── invoices.db
├── requirements.txt
└── README.md
```

