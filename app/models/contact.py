# app/models/contact.py
# ─────────────────────────────────────────────────────────────
# This defines the "contacts" table in our database.
# A contact can be:
#   - EMERGENCY  → Police (100), Fire (101), Ambulance (108)
#   - OFFICIAL   → Mukhiya, BDO, Sarpanch, Patwari
#   - HEALTH     → Doctor, PHC, ASHA worker
#   - EDUCATION  → School principal, Anganwadi
# All contacts are added manually by Admin after visiting the
# person/office and getting their permission (where needed).
# ─────────────────────────────────────────────────────────────

import enum
from sqlalchemy import Column, Integer, String, Boolean, Text, Enum, DateTime
from sqlalchemy.sql import func
from app.database import Base


class ContactCategory(str, enum.Enum):
    """
    What type of contact is this?
    Used by the Flutter app to group contacts into sections.
    """
    emergency = "emergency"     # Police 100, Fire 101, Ambulance 108
    official = "official"       # Mukhiya, BDO, Sarpanch, Patwari
    health = "health"           # Doctor, PHC, ASHA worker
    education = "education"     # School principal, Anganwadi
    service_provider = "service_provider"  # ✅ ADD THIS LINE — plumbers, doctors, electricians


class Contact(Base):
    __tablename__ = "contacts"

    # — Identity ──────────────────────────────────────────────
    # Integer ID — consistent with all other models (schemes, weather, etc.)
    id = Column(Integer, primary_key=True, index=True)

    # Village tag — every record belongs to a village
    # Enables multi-village use in the future without schema changes
    village_id = Column(Integer, nullable=False, default=1)

    # — Core contact information ───────────────────────────────
    name = Column(String, nullable=False)           # "Ram Prasad Singh" or "Durbe Police Chowki"
    designation = Column(String, nullable=False)    # "Mukhiya" or "Police Station"
    phone = Column(String, nullable=True)           # "100" or "9876543210" — nullable for offices with no direct number
    category = Column(Enum(ContactCategory), nullable=False)

    # — Location and timing ───────────────────────────────────
    address = Column(Text, nullable=True)           # "Near Bus Stand, Atri, Gaya"
    office_hours = Column(String, nullable=True)    # "10am–5pm, Mon–Sat"

    # — Permission flag ───────────────────────────────────────
    # False → public number (Police 100) — no consent needed, Admin adds directly
    # True  → personal contact (Mukhiya) — Admin visited and got their permission first
    requires_permission = Column(Boolean, default=True, nullable=False)

    # — How to talk guide ─────────────────────────────────────
    # Admin writes step-by-step instructions for villagers.
    # Example: "1. State your name and village\n2. Describe the issue\n3. Ask for complaint number"
    # Shown in the app as a guide card below the contact details.
    how_to_talk = Column(Text, nullable=True)

    # — Visibility ────────────────────────────────────────────
    # Soft delete — Admin can hide a contact without deleting it from the database.
    # is_active = False means the contact won't appear in the app.
    is_active = Column(Boolean, default=True, nullable=False)

    # — Timestamps ────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())