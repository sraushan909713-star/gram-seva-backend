# app/schemas/contact.py
# ─────────────────────────────────────────────────────────────
# Pydantic schemas — define the shape of data coming IN and going OUT
# of the contacts API.
#
# ContactCreate  → data Admin sends when adding a new contact
# ContactUpdate  → data Admin sends when editing a contact (all fields optional)
# ContactResponse → what the API sends back to the Flutter app
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.contact import ContactCategory


# — REQUEST SCHEMAS (data coming IN from Admin) ───────────────

class ContactCreate(BaseModel):
    """
    Used when Admin creates a new contact via POST /contacts.
    Admin must visit the person/office first and get permission before adding.
    """
    name: str                               # Person or office name
    designation: str                        # e.g. "Mukhiya", "Police Station"
    phone: Optional[str] = None             # Contact number (optional — some offices have no direct line)
    category: ContactCategory               # emergency / official / health / education
    address: Optional[str] = None           # Physical address
    office_hours: Optional[str] = None      # e.g. "10am–5pm, Mon–Sat"
    requires_permission: bool = True        # False for public numbers like 100, 108
    how_to_talk: Optional[str] = None       # Step-by-step guide for villagers
    village_id: int = 1                     # Defaults to Durbe village


class ContactUpdate(BaseModel):
    """
    Used when Admin edits a contact via PUT /contacts/{id}.
    All fields are optional — only send what needs to change.
    """
    name: Optional[str] = None
    designation: Optional[str] = None
    phone: Optional[str] = None
    category: Optional[ContactCategory] = None
    address: Optional[str] = None
    office_hours: Optional[str] = None
    requires_permission: Optional[bool] = None
    how_to_talk: Optional[str] = None


# — RESPONSE SCHEMA (data going OUT to Flutter app) ───────────

class ContactResponse(BaseModel):
    """
    Returned by the API in every contact response.
    The Flutter app uses this to display the contact card and how-to-talk guide.
    """
    id: int
    village_id: int
    name: str
    designation: str
    phone: Optional[str]
    category: ContactCategory
    address: Optional[str]
    office_hours: Optional[str]
    requires_permission: bool
    how_to_talk: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True  # Allows SQLAlchemy model → Pydantic conversion