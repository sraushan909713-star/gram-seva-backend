# app/models/gram_sabha.py
# ─────────────────────────────────────────────
# Gram Sabha = Official Village Assembly Records
# These are official meeting records added by Admin only.
# Making attendance and decisions visible holds elected
# representatives accountable to the villagers they serve.
# ─────────────────────────────────────────────

import uuid
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class GramSabha(Base):
    __tablename__ = "gram_sabha"

    # ── Identity ──────────────────────────────
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # ── Meeting information ────────────────────
    title = Column(String, nullable=False)           # e.g. "Quarterly Gram Sabha — Jan 2026"
    meeting_date = Column(Date, nullable=False)      # When the meeting happened
    location = Column(String, nullable=False)        # Where it was held in Durbe
    agenda = Column(Text, nullable=False)            # Topics discussed in the meeting
    decisions = Column(Text, nullable=False)         # Official decisions taken
    attendees_count = Column(Integer, nullable=False) # How many people attended
    minutes_url = Column(String, nullable=True)      # Link to official minutes doc (optional)

    # ── Ownership ─────────────────────────────
    # Only Admin adds these — they are official records, not user posts
    created_by = Column(String, ForeignKey("users.id"), nullable=False)
    creator = relationship("User", backref="gram_sabha_records")

    # ── Visibility ────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)

    # ── Timestamps ────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())