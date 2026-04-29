# app/schemas/guide.py
# ─────────────────────────────────────────────────────────────
# Pydantic schemas — define the shape of data coming IN and going OUT
# of the guides API.
#
# GuideCreate      → data Admin sends when adding a new guide
# GuideUpdate      → data Admin sends when editing (all fields optional)
# GuideResponse    → full detail returned by the API (single guide view)
# GuideListResponse → lightweight version for the list screen
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.guide import GuideCategory


# — REQUEST SCHEMAS (data coming IN from Admin) ───────────────

class GuideCreate(BaseModel):
    """
    Used when Admin creates a new guide via POST /guides.
    Admin must visit the office first before writing these details.
    """
    title: str                                  # "Jati Praman Patra"
    title_hindi: Optional[str] = None           # "जाति प्रमाण पत्र"
    description: str                            # Brief summary of what this document is
    category: GuideCategory                     # certificate / welfare / land / education / health / other
    office_name: Optional[str] = None           # "Block Development Office, Atri"
    office_address: Optional[str] = None        # "Near Bus Stand, Atri, Gaya"
    contact_person: Optional[str] = None        # "Clerk at Counter 3"
    timings: Optional[str] = None               # "10am–4pm, Mon–Fri"
    approximate_cost: Optional[str] = None      # "₹0 (Free)" or "₹50 for notary"
    steps: str                                  # Full step-by-step process
    documents_needed: Optional[str] = None      # Comma-separated list
    tips: Optional[str] = None                  # Insider advice from Admin
    village_id: str = "1"                       # Defaults to Durbe village


class GuideUpdate(BaseModel):
    """
    Used when Admin edits a guide via PUT /guides/{id}.
    All fields are optional — only send what needs to change.
    """
    title: Optional[str] = None
    title_hindi: Optional[str] = None
    description: Optional[str] = None
    category: Optional[GuideCategory] = None
    office_name: Optional[str] = None
    office_address: Optional[str] = None
    contact_person: Optional[str] = None
    timings: Optional[str] = None
    approximate_cost: Optional[str] = None
    steps: Optional[str] = None
    documents_needed: Optional[str] = None
    tips: Optional[str] = None
    is_active: Optional[bool] = None            # Admin can hide/show a guide


# — RESPONSE SCHEMAS (data going OUT to Flutter app) ──────────

class GuideResponse(BaseModel):
    """
    Returned when viewing a single guide — full detail view.
    This is what the Flutter app shows when user taps on a guide.
    """
    id: str
    village_id: str
    title: str
    title_hindi: Optional[str]
    description: str
    category: GuideCategory
    office_name: Optional[str]
    office_address: Optional[str]
    contact_person: Optional[str]
    timings: Optional[str]
    approximate_cost: Optional[str]
    steps: str
    documents_needed: Optional[str]
    tips: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True      # Allows SQLAlchemy model → Pydantic conversion


class GuideListResponse(BaseModel):
    """
    Returned by GET /guides — lightweight summary for the list screen.
    Excludes heavy fields like steps and tips to keep response fast.
    Flutter fetches full detail only when user taps on a guide.
    """
    id: str
    village_id: str
    title: str
    title_hindi: Optional[str]
    description: str
    category: GuideCategory
    office_name: Optional[str]
    timings: Optional[str]
    approximate_cost: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True