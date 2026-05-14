# app/schemas/banner.py
# ─────────────────────────────────────────────────────────────
# Pydantic schemas for Home Screen Banners.
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class BannerCreate(BaseModel):
    """Super Admin creates a new banner."""
    title:           str
    subtitle:        Optional[str]      = None
    icon:            Optional[str]      = None      # Emoji e.g. "💼"
    image_url:       Optional[str]      = None      # Cloudinary URL
    bg_color_start:  Optional[str]      = None      # Hex e.g. "#1E3A5F"
    bg_color_end:    Optional[str]      = None      # Hex e.g. "#166534"
    redirect_type:   Optional[str]      = None      # "internal" or "external"
    redirect_target: Optional[str]      = None      # screen name or URL
    display_order:   int                = 0
    tag:             Optional[str]      = None
    valid_until:     Optional[datetime] = None
    village_id:      str                = "1"


class BannerUpdate(BaseModel):
    """Super Admin edits a banner — all fields optional."""
    title:           Optional[str]      = None
    subtitle:        Optional[str]      = None
    icon:            Optional[str]      = None
    image_url:       Optional[str]      = None
    bg_color_start:  Optional[str]      = None
    bg_color_end:    Optional[str]      = None
    redirect_type:   Optional[str]      = None
    redirect_target: Optional[str]      = None
    display_order:   Optional[int]      = None
    tag:             Optional[str]      = None
    valid_until:     Optional[datetime] = None
    is_active:       Optional[bool]     = None


class BannerResponse(BaseModel):
    """Full banner response sent to Flutter."""
    id:              str
    village_id:      str
    title:           str
    subtitle:        Optional[str]
    icon:            Optional[str]
    image_url:       Optional[str]
    bg_color_start:  Optional[str]
    bg_color_end:    Optional[str]
    redirect_type:   Optional[str]
    redirect_target: Optional[str]
    display_order:   int
    tag:             Optional[str]
    valid_until:     Optional[datetime]
    is_active:       bool
    created_at:      datetime

    class Config:
        from_attributes = True