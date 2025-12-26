from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    vendor = Column(String)
    invoice_number = Column(String)
    invoice_date = Column(String)
    tax_percent = Column(Float)
    anomaly = Column(String)
    raw_text = Column(String)