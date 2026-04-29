# app/models/vikas_prastav.py
# ─────────────────────────────────────────────
# Vikas Prastav = "Development Proposal"
# Villagers propose development projects they want built.
# Upvotes represent community mandate — the more support,
# the stronger the case for funding and action.
# ─────────────────────────────────────────────

import uuid
import enum
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class ProposalCategory(str, enum.Enum):
    """
    Type of development being proposed.
    Helps officials and villagers filter by their area of interest.
    """
    road          = "road"          # Roads, paths, bridges
    water         = "water"         # Wells, pumps, pipelines
    education     = "education"     # Schools, classrooms, libraries
    health        = "health"        # Health centres, toilets
    electricity   = "electricity"   # Streetlights, power supply
    agriculture   = "agriculture"   # Irrigation, storage
    other         = "other"         # Any other development


class VikasPrastav(Base):
    __tablename__ = "vikas_prastav"

    # ── Identity ──────────────────────────────
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # ── Core proposal information ──────────────
    title = Column(String, nullable=False)           # Short proposal headline
    description = Column(Text, nullable=False)       # Full proposal details
    location = Column(String, nullable=False)        # Where in Durbe
    category = Column(
        Enum(ProposalCategory),
        nullable=False
    )                                                # Type of development
    estimated_cost = Column(String, nullable=True)   # Rough cost e.g. "₹2-3 lakh" (optional)
    funding_source = Column(String, nullable=True)   # e.g. "MGNREGA", "14th Finance Commission"
    photo_url_1 = Column(String, nullable=False)     # Photo of area — MANDATORY
    photo_url_2 = Column(String, nullable=True)      # Optional
    photo_url_3 = Column(String, nullable=True)      # Optional
    photo_url_4 = Column(String, nullable=True)      # Optional
    
    # ── Community support ─────────────────────
    upvote_count = Column(Integer, default=0, nullable=False)

    # ── Ownership ─────────────────────────────
    posted_by = Column(String, ForeignKey("users.id"), nullable=False)
    poster = relationship("User", backref="vikas_prastav_posts")

    # ── Visibility ────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)

    # ── Timestamps ────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class VikasPrastavUpvote(Base):
    """
    Tracks who upvoted which proposal.
    Prevents duplicate upvotes — one user, one upvote per proposal.
    """
    __tablename__ = "vikas_prastav_upvotes"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    post_id = Column(String, ForeignKey("vikas_prastav.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())