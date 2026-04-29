# app/models/gram_awaaz.py
# ─────────────────────────────────────────────
# Gram Awaaz = "Village Voice"
# A civic complaint/issue board where verified villagers can raise
# problems, tag responsible departments, and collect upvotes.
#
# Design principles:
# - Evidence over emotion: location, affected count, photo are required
# - Named accountability: department field is mandatory
# - Upvote = pressure: upvote count is tracked separately to prevent fraud
# ─────────────────────────────────────────────

import uuid
import enum
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Department(str, enum.Enum):
    """
    The government body responsible for resolving the issue.
    Making this mandatory ensures every complaint has a named target.
    """
    panchayat   = "panchayat"     # Gram Panchayat
    bdo         = "bdo"           # Block Development Office
    pwd         = "pwd"           # Public Works Department (roads)
    health      = "health"        # Primary Health Centre
    police      = "police"        # Police Station
    education   = "education"     # School / Education Dept
    electricity = "electricity"   # Bijli department
    water       = "water"         # Jal Jeevan / water supply
    other       = "other"         # Any other department


class GramAwaaz(Base):
    __tablename__ = "gram_awaaz"

    # ── Identity ──────────────────────────────
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # ── Core complaint information ─────────────
    title = Column(String, nullable=False)          # Short headline of the issue
    description = Column(Text, nullable=False)      # Full story in user's own words
    location = Column(String, nullable=False)       # Specific area within Durbe
    affected_count = Column(Integer, nullable=False) # How many people are affected
    department = Column(
        Enum(Department),
        nullable=False
    )                                               # Which dept is responsible
    demand = Column(Text, nullable=False)           # Specific ask — what should happen
    # Cloudinary URLs stored directly — fast optimized delivery
    photo_url_1 = Column(String, nullable=False)     # Evidence photo — MANDATORY
    photo_url_2 = Column(String, nullable=True)      # Optional
    photo_url_3 = Column(String, nullable=True)      # Optional
    photo_url_4 = Column(String, nullable=True)      # Optional

    # ── Engagement ────────────────────────────
    upvote_count = Column(Integer, default=0, nullable=False)  # Total upvotes received

    # ── Ownership ─────────────────────────────
    posted_by = Column(String, ForeignKey("users.id"), nullable=False)
    poster = relationship("User", backref="gram_awaaz_posts")

    # ── Visibility ────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)

    # ── Timestamps ────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class GramAwaazUpvote(Base):
    """
    Tracks who upvoted which post.
    Prevents the same user from upvoting the same post twice.
    Each row = one user upvoted one post.
    """
    __tablename__ = "gram_awaaz_upvotes"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    post_id = Column(String, ForeignKey("gram_awaaz.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())