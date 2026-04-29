# app/schemas/job_alert.py
#
# ──────────────────────────────────────────────────────────────────
# Pydantic schemas — shape of data IN and OUT of the Job Alerts API.
#
# JobAlertCreate         → Admin adds a new job posting
# JobAlertUpdate         → Admin edits (all fields optional)
# JobAlertListResponse   → Lightweight card for the list screen
# JobAlertResponse       → Full detail when user taps a job card
# JobApplicantCreate     → Admin adds an applicant (after WhatsApp proof)
# JobApplicantResponse   → Applicant shown in social proof section
# ──────────────────────────────────────────────────────────────────

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from app.models.job_alert import JobCategory


# ─── Job Alert Request Schemas ────────────────────────────────────

class JobAlertCreate(BaseModel):
    """Admin creates a new job posting."""
    title:        str
    organization: str
    category:     JobCategory
    total_posts:  Optional[int]  = None
    eligibility:  str
    how_to_apply: str
    apply_link:   Optional[str] = None
    last_date:    date
    salary_range: Optional[str] = None
    notes:        Optional[str] = None
    village_id:   int           = 1


class JobAlertUpdate(BaseModel):
    """Admin edits an existing job posting — all fields optional."""
    title:        Optional[str]         = None
    organization: Optional[str]         = None
    category:     Optional[JobCategory] = None
    total_posts:  Optional[int]         = None
    eligibility:  Optional[str]         = None
    how_to_apply: Optional[str]         = None
    apply_link:   Optional[str]         = None
    last_date:    Optional[date]        = None
    salary_range: Optional[str]         = None
    notes:        Optional[str]         = None


# ─── Job Alert Response Schemas ───────────────────────────────────

class JobAlertListResponse(BaseModel):
    """
    Lightweight card for the list screen.
    Shows enough for youth to decide if worth tapping.
    """
    id:           str
    title:        str
    organization: str
    category:     JobCategory
    total_posts:  Optional[int]     = None
    last_date:    date
    salary_range: Optional[str]     = None
    is_active:    bool
    created_at:   datetime

    class Config:
        from_attributes = True


class JobAlertResponse(BaseModel):
    """Full detail — shown when user taps a job card."""
    id:           str
    village_id:   int
    title:        str
    organization: str
    category:     JobCategory
    total_posts:  Optional[int]     = None
    eligibility:  str
    how_to_apply: str
    apply_link:   Optional[str]     = None
    last_date:    date
    salary_range: Optional[str]     = None
    notes:        Optional[str]     = None
    is_active:    bool
    created_at:   datetime
    updated_at:   Optional[datetime] = None

    class Config:
        from_attributes = True


# ─── Job Applicant Schemas ────────────────────────────────────────

class JobApplicantCreate(BaseModel):
    """
    Admin adds a villager who has applied for this job.
    Called after villager sends WhatsApp proof to Admin.
    gram_seva_user_id is optional — non-app villagers can also be added.
    """
    name:              str
    relative_name:     Optional[str] = None
    gender:            str           = "male"
    photo_url:         Optional[str] = None
    gram_seva_user_id: Optional[str] = None
    applied_date:      Optional[date] = None


class JobApplicantResponse(BaseModel):
    """Applicant shown in the social proof section of job detail."""
    id:                str
    job_id:            str
    name:              str
    relative_name:     Optional[str]  = None
    gender:            str
    photo_url:         Optional[str]  = None
    gram_seva_user_id: Optional[str]  = None
    applied_date:      Optional[date] = None
    is_active:         bool
    created_at:        datetime

    class Config:
        from_attributes = True