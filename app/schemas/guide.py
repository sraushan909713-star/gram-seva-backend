# app/schemas/guide.py
# ─────────────────────────────────────────────────────────────
# Pydantic schemas for Documentation Guides API.
#
# GuideCreate       → Admin adds a new guide
# GuideUpdate       → Admin edits (all fields optional)
# GuideListResponse → Lightweight card for list screen
# GuideResponse     → Full detail when user taps a guide
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.guide import GuideCategory


# ─── Request Schemas ─────────────────────────────────────────

class GuideCreate(BaseModel):
    """Admin creates a new documentation guide."""
    title:            str
    title_hindi:      Optional[str] = None
    description:      str
    category:         GuideCategory
    office_name:      Optional[str] = None
    office_address:   Optional[str] = None
    contact_person:   Optional[str] = None
    timings:          Optional[str] = None
    approximate_cost: Optional[str] = None
    estimated_time:   Optional[str] = None      # ✅ NEW
    steps:            str
    documents_needed: Optional[str] = None
    online_link:      Optional[str] = None      # ✅ NEW
    tips:             Optional[str] = None
    village_id:       str            = "1"


class GuideUpdate(BaseModel):
    """Admin edits a guide — all fields optional."""
    title:            Optional[str]           = None
    title_hindi:      Optional[str]           = None
    description:      Optional[str]           = None
    category:         Optional[GuideCategory] = None
    office_name:      Optional[str]           = None
    office_address:   Optional[str]           = None
    contact_person:   Optional[str]           = None
    timings:          Optional[str]           = None
    approximate_cost: Optional[str]           = None
    estimated_time:   Optional[str]           = None  # ✅ NEW
    steps:            Optional[str]           = None
    documents_needed: Optional[str]           = None
    online_link:      Optional[str]           = None  # ✅ NEW
    tips:             Optional[str]           = None
    is_active:        Optional[bool]          = None


# ─── Response Schemas ─────────────────────────────────────────

class GuideListResponse(BaseModel):
    """Lightweight card for list screen — no steps to keep it fast."""
    id:               str
    village_id:       str
    title:            str
    title_hindi:      Optional[str]
    description:      str
    category:         GuideCategory
    office_name:      Optional[str]
    timings:          Optional[str]
    approximate_cost: Optional[str]
    estimated_time:   Optional[str]           # ✅ NEW
    online_link:      Optional[str]           # ✅ NEW — so Flutter shows "Online" badge
    is_active:        bool

    class Config:
        from_attributes = True


class GuideResponse(BaseModel):
    """Full detail — shown when user taps a guide card."""
    id:               str
    village_id:       str
    title:            str
    title_hindi:      Optional[str]
    description:      str
    category:         GuideCategory
    office_name:      Optional[str]
    office_address:   Optional[str]
    contact_person:   Optional[str]
    timings:          Optional[str]
    approximate_cost: Optional[str]
    estimated_time:   Optional[str]           # ✅ NEW
    steps:            str
    documents_needed: Optional[str]
    online_link:      Optional[str]           # ✅ NEW
    tips:             Optional[str]
    is_active:        bool
    created_at:       datetime
    updated_at:       Optional[datetime]      = None

    class Config:
        from_attributes = True