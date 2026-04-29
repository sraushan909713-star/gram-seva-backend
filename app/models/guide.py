# app/models/guide.py
# ─────────────────────────────────────────────────────────────
# This defines the "guides" table in our database.
# A guide is a step-by-step documentation written by Admin
# to help villagers apply for government certificates and services.
# Examples: Jati Praman Patra, Awaasiye Praman Patra, Ration Card
# All guides are added manually by Admin after visiting the office.
# ─────────────────────────────────────────────────────────────

import uuid
import enum
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base


class GuideCategory(str, enum.Enum):
    """
    What type of documentation is this guide for?
    Used by the Flutter app to group guides into sections.
    """
    certificate = "certificate"     # Jati, Awaasiye, Janm Praman Patra
    welfare     = "welfare"         # Ration card, Pension, BPL card
    land        = "land"            # Land records, Khasra, Naksha
    education   = "education"       # Scholarship, School admission
    health      = "health"          # Ayushman card, PHC registration
    other       = "other"           # Anything that doesn't fit above


class Guide(Base):
    __tablename__ = "guides"

    # — Identity ──────────────────────────────────────────────
    # UUID string ID — same pattern as schemes model
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # — Village tag ───────────────────────────────────────────
    # Every record belongs to a village — same pattern as all models
    village_id = Column(String, nullable=False, default="1")

    # — Core guide information ─────────────────────────────────
    title = Column(String, nullable=False)              # "Jati Praman Patra"
    title_hindi = Column(String, nullable=True)         # "जाति प्रमाण पत्र"
    description = Column(Text, nullable=False)          # Brief summary of what this document is
    category = Column(
        Enum(GuideCategory),
        nullable=False,
        default=GuideCategory.other
    )

    # — Office details ────────────────────────────────────────
    # Admin fills these after visiting the office in person
    office_name = Column(String, nullable=True)         # "Block Development Office, Atri"
    office_address = Column(Text, nullable=True)        # "Near Bus Stand, Atri, Gaya"
    contact_person = Column(String, nullable=True)      # "Clerk at Counter 3" (optional)
    timings = Column(String, nullable=True)             # "10am–4pm, Mon–Fri"
    approximate_cost = Column(String, nullable=True)    # "₹0 (Free)" or "₹50 for notary"

    # — The step-by-step process ──────────────────────────────
    # Admin writes the exact steps a villager must follow.
    # Stored as plain text with numbered steps.
    # Example: "1. Go to BDO office\n2. Ask for Form 16\n3. Fill form..."
    steps = Column(Text, nullable=False)

    # — Documents needed ──────────────────────────────────────
    # Comma-separated list of documents required.
    # Example: "Aadhar Card, Ration Card, Passport Photo, Father's name proof"
    documents_needed = Column(Text, nullable=True)

    # — Tips from Admin ───────────────────────────────────────
    # Insider advice Admin learned from visiting the office.
    # Example: "Go before 11am — gets very crowded after lunch"
    tips = Column(Text, nullable=True)

    # — Visibility ────────────────────────────────────────────
    # Soft delete — same pattern as schemes and contacts
    is_active = Column(Boolean, default=True, nullable=False)

    # — Timestamps ────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    