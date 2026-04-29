# app/schemas/gram_sabha.py
# ─────────────────────────────────────────────
# Pydantic schemas for Gram Sabha Records feature.
# ─────────────────────────────────────────────

from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime


# ── REQUEST SCHEMAS ────────────────────────────────────────────

class GramSabhaCreate(BaseModel):
    """
    Used when Admin adds a new Gram Sabha meeting record.
    """
    title: str                              # Meeting title
    meeting_date: date                      # Date of the meeting
    location: str                           # Where it was held
    agenda: str                             # Topics discussed
    decisions: str                          # Official decisions taken
    attendees_count: int                    # How many attended
    minutes_url: Optional[str] = None       # Link to official minutes (optional)


class GramSabhaUpdate(BaseModel):
    """
    Used when Admin edits a record via PUT /gram-sabha/{id}.
    All fields optional — only send what needs to change.
    """
    title: Optional[str] = None
    meeting_date: Optional[date] = None
    location: Optional[str] = None
    agenda: Optional[str] = None
    decisions: Optional[str] = None
    attendees_count: Optional[int] = None
    minutes_url: Optional[str] = None
    is_active: Optional[bool] = None


# ── RESPONSE SCHEMAS ───────────────────────────────────────────

class GramSabhaListResponse(BaseModel):
    """
    Lightweight summary for the records list screen.
    Shows enough to identify the meeting without heavy text.
    """
    id: str
    title: str
    meeting_date: date
    location: str
    attendees_count: int
    created_at: datetime

    class Config:
        from_attributes = True


class GramSabhaResponse(BaseModel):
    """
    Full meeting record — shown when user taps on a record.
    """
    id: str
    title: str
    meeting_date: date
    location: str
    agenda: str
    decisions: str
    attendees_count: int
    minutes_url: Optional[str] = None
    created_by: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True