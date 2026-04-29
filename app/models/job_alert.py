# app/models/job_alert.py
#
# ──────────────────────────────────────────────────────────────────
# Job Alerts — Sarkari Naukri notifications for Durbe village youth.
#
# Tables:
#   job_alerts      → job postings added by Admin/Super Admin
#   job_applicants  → villagers who applied (social proof section)
#
# Design principles:
# - last_date is the most critical field — always shown prominently
# - category helps youth filter what's relevant to them
# - is_active = False for expired jobs (soft delete pattern)
# - JobApplicant added by Admin after WhatsApp proof verification
# ──────────────────────────────────────────────────────────────────

import enum
import uuid
from sqlalchemy import Column, String, Text, Integer, Boolean, Date, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


# ─── Job Category Enum ────────────────────────────────────────────

class JobCategory(str, enum.Enum):
    """
    What type of job is this?
    Shown as filter chips in the Flutter app.
    """
    government = "government"   # Central/State government jobs
    private    = "private"      # Private sector jobs
    railway    = "railway"      # Indian Railways recruitment
    banking    = "banking"      # Bank PO, clerk, RRB etc.
    defence    = "defence"      # Army, CRPF, Police
    teaching   = "teaching"     # Teacher recruitment, TET
    other      = "other"        # Any other opportunity


# ─── Job Alert ───────────────────────────────────────────────────

class JobAlert(Base):
    __tablename__ = "job_alerts"

    # — Identity ──────────────────────────────────────────────────
    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    village_id = Column(Integer, nullable=False, default=1)

    # — Core job information ───────────────────────────────────────
    title        = Column(String, nullable=False)   # "SSC CHSL Recruitment 2025"
    organization = Column(String, nullable=False)   # "Staff Selection Commission"
    category     = Column(Enum(JobCategory), nullable=False)

    # — Key details villagers need ─────────────────────────────────
    total_posts  = Column(Integer, nullable=True)   # Total number of vacancies
    eligibility  = Column(Text, nullable=False)     # Age, education requirements
    how_to_apply = Column(Text, nullable=False)     # Step-by-step application guide
    apply_link   = Column(String, nullable=True)    # Direct URL to apply online
    last_date    = Column(Date, nullable=False)     # APPLICATION DEADLINE — critical

    # — Optional extra info ────────────────────────────────────────
    salary_range = Column(String, nullable=True)    # "₹25,000 – ₹35,000/month"
    notes        = Column(Text, nullable=True)      # Any extra important info

    # — Visibility ─────────────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)

    # — Timestamps ─────────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # — Relationships ──────────────────────────────────────────────
    applicants = relationship("JobApplicant", back_populates="job",
                              cascade="all, delete-orphan")


# ─── Job Applicant ───────────────────────────────────────────────

class JobApplicant(Base):
    """
    Records villagers who have applied for a job.
    Added by Admin after villager sends WhatsApp proof.
    Two types:
      - Gram Seva user   → gram_seva_user_id is set
      - Non-app villager → just name + relative_name stored manually
    """
    __tablename__ = "job_applicants"

    # — Identity ──────────────────────────────────────────────────
    id     = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = Column(String, ForeignKey("job_alerts.id"), nullable=False)

    # — Villager info (always filled) ─────────────────────────────
    name          = Column(String, nullable=False)   # Full name
    relative_name = Column(String, nullable=True)    # Father/Husband name
    gender        = Column(String(6), nullable=False, default="male")
    photo_url     = Column(String, nullable=True)    # Cloudinary URL (optional)

    # — Gram Seva account link (optional) ─────────────────────────
    # Set if the applicant has a Gram Seva account
    gram_seva_user_id = Column(String, ForeignKey("users.id"), nullable=True)

    # — Applied on ────────────────────────────────────────────────
    applied_date = Column(Date, nullable=True)       # When they submitted the application

    # — Visibility ─────────────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)

    # — Timestamps ─────────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # — Relationships ──────────────────────────────────────────────
    job  = relationship("JobAlert", back_populates="applicants")
    user = relationship("User", backref="job_applications")
    