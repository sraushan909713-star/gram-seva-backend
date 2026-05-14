# app/models/guide.py
# ─────────────────────────────────────────────────────────────
# Documentation Guides — step-by-step help for villagers
# to apply for government certificates and services.
#
# Admin adds guides after visiting the office in person.
# Villagers can browse and follow the steps from the app.
#
# Fields added vs original:
#   - online_link: optional URL for documents that can be applied online
#   - Updated GuideCategory enum with specific document types
# ─────────────────────────────────────────────────────────────

import uuid
import enum
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base


# ─── Guide Category Enum ──────────────────────────────────────

class GuideCategory(str, enum.Enum):
    """
    What type of document is this guide for?
    Shown as filter chips in the Flutter app.
    """
    ration_card        = "ration_card"
    birth_certificate  = "birth_certificate"
    caste_certificate  = "caste_certificate"
    income_certificate = "income_certificate"
    aadhaar            = "aadhaar"
    pension            = "pension"
    land_records       = "land_records"
    health             = "health"
    education          = "education"
    other              = "other"


# ─── Guide Model ─────────────────────────────────────────────

class Guide(Base):
    __tablename__ = "guides"

    # — Identity ──────────────────────────────────────────────
    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    village_id = Column(String, nullable=False, default="1")

    # — Core guide information ─────────────────────────────────
    title        = Column(String, nullable=False)   # "Jati Praman Patra"
    title_hindi  = Column(String, nullable=True)    # "जाति प्रमाण पत्र"
    description  = Column(Text,   nullable=False)   # Brief summary
    category     = Column(Enum(GuideCategory), nullable=False, default=GuideCategory.other)

    # — Office details ────────────────────────────────────────
    office_name    = Column(String, nullable=True)  # "Block Development Office, Atri"
    office_address = Column(Text,   nullable=True)  # "Near Bus Stand, Atri, Gaya"
    contact_person = Column(String, nullable=True)  # "Clerk at Counter 3"
    timings        = Column(String, nullable=True)  # "10am–4pm, Mon–Fri"

    # — Cost & time ───────────────────────────────────────────
    approximate_cost = Column(String, nullable=True)  # "₹0 (Free)" or "₹50 for notary"
    estimated_time   = Column(String, nullable=True)  # "7–10 working days"

    # — Step-by-step process ──────────────────────────────────
    # Stored as plain text with numbered steps.
    # e.g. "1. Go to BDO office\n2. Ask for Form 16\n3. Fill form..."
    steps = Column(Text, nullable=False)

    # — Documents needed ──────────────────────────────────────
    # Newline or comma separated list of required documents
    documents_needed = Column(Text, nullable=True)

    # — Online application link ───────────────────────────────  ✅ NEW
    # Optional — some documents can be applied online
    # e.g. "https://serviceonline.bihar.gov.in"
    online_link = Column(String, nullable=True)

    # — Tips from Admin ───────────────────────────────────────
    # Insider advice from visiting the office
    # e.g. "Go before 11am — gets very crowded after lunch"
    tips = Column(Text, nullable=True)

    # — Visibility ────────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)

    # — Timestamps ────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    