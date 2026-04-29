# app/schemas/community_member.py
#
# ──────────────────────────────────────────────────────────────────
# Pydantic schemas — shape of data IN and OUT of Community Members API.
#
# CommunityMemberCreate  → Admin sends when adding a member
# CommunityMemberResponse → What the app shows in the members list
# ──────────────────────────────────────────────────────────────────

from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import date, datetime
from app.models.community_member import Gender


# — REQUEST SCHEMA ────────────────────────────────────────────────

class CommunityMemberCreate(BaseModel):
    """
    Admin adds a member to a Job Alert or Scheme.
    Either job_id OR scheme_id must be provided — not both, not neither.
    """
    job_id:    Optional[str] = None   # ✅ provide one of these
    scheme_id: Optional[str] = None   # ✅ provide one of these

    name:          str
    relative_name: str                # Pita ka naam or Pati ka naam
    gender:        Gender
    since_date:    date               # Full date: DD/MM/YYYY

    # ✅ Optional — only if person is on Gram Seva
    gram_seva_user_id: Optional[str] = None
    photo_url:         Optional[str] = None

    village_id: str = "1"

    @model_validator(mode='after')
    def check_job_or_scheme(self):
        """
        Validation rule: exactly one of job_id or scheme_id must be set.
        An entry cannot belong to both a job and a scheme simultaneously.
        """
        if self.job_id and self.scheme_id:
            raise ValueError('Provide either job_id OR scheme_id — not both.')
        if not self.job_id and not self.scheme_id:
            raise ValueError('Either job_id or scheme_id must be provided.')
        return self


# — RESPONSE SCHEMA ───────────────────────────────────────────────

class CommunityMemberResponse(BaseModel):
    """
    Shown in the members list under a Job Alert or Scheme.
    Visible to everyone — no login required.
    """
    id:               str
    job_id:           Optional[str]
    scheme_id:        Optional[str]
    name:             str
    relative_name:    str
    gender:           Gender
    since_date:       date
    gram_seva_user_id: Optional[str]
    photo_url:        Optional[str]
    added_by_admin_id: str
    is_active:        bool
    created_at:       datetime

    class Config:
        from_attributes = True
        