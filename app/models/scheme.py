# app/models/scheme.py
# ─────────────────────────────────────────────
# This defines the "schemes" table in our database.
# Each row represents one government scheme (e.g. PM Kisan, Ayushman Bharat).
# Only Admins and Super Admins can add/edit/delete schemes.
# Villagers can only read them.
# ─────────────────────────────────────────────

import uuid
import enum
from sqlalchemy import Column, String, Text, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.database import Base


class SchemeCategory(str, enum.Enum):
    """
    Fixed list of categories a scheme can belong to.
    Using an Enum ensures no typos or inconsistent values in the database.
    """
    health      = "health"
    farming     = "farming"
    education   = "education"
    housing     = "housing"
    finance     = "finance"
    women       = "women"
    other       = "other"


class Scheme(Base):
    __tablename__ = "schemes"

    # ── Identity ──────────────────────────────
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())  # Auto-generate unique ID
    )

    # ── Core scheme information ────────────────
    name = Column(String, nullable=False)           # e.g. "PM Kisan Samman Nidhi"
    description = Column(Text, nullable=False)      # What this scheme does
    eligibility = Column(Text, nullable=False)      # Who can apply
    how_to_apply = Column(Text, nullable=False)     # Steps to apply
    official_link = Column(String, nullable=True)   # Government website (optional)
    additional_info = Column(Text, nullable=True)   # Any extra details (optional)
    youtube_link = Column(String, nullable=True)   # YouTube guide video (optional)   # ✅ ADD
    documents_required = Column(Text, nullable=False, server_default="Not specified")  # ✅ ADD — docs needed to apply

    # ── Category ──────────────────────────────
    category = Column(
        Enum(SchemeCategory),
        nullable=False,
        default=SchemeCategory.other
    )

    # ── Visibility ────────────────────────────
    # Instead of deleting a scheme, admin can set is_active=False to hide it.
    # This preserves data history without showing outdated schemes to villagers.
    is_active = Column(Boolean, default=True, nullable=False)

    # ── Timestamps ────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    