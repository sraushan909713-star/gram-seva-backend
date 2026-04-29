# app/schemas/neta_report_card.py
# ─────────────────────────────────────────────────────────────
# Pydantic schemas for Neta Ka Report Card feature.
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime


# ─── Neta (Leader) Schemas ───────────────────────────────────

class NetaCreate(BaseModel):
    """Admin creates a new leader entry."""
    name:        str
    designation: str            # Sarpanch / Ward Member / MLA / MP / Other
    party:       Optional[str] = None
    photo_url:   Optional[str] = None


class NetaUpdate(BaseModel):
    """Admin updates an existing leader entry."""
    name:        Optional[str] = None
    designation: Optional[str] = None
    party:       Optional[str] = None
    photo_url:   Optional[str] = None


class NetaResponse(BaseModel):
    """Full leader detail — used in list and detail screens."""
    id:             str
    name:           str
    designation:    str
    party:          Optional[str] = None
    photo_url:      Optional[str] = None
    average_rating: Optional[float] = None     # Computed — avg of all active ratings
    total_ratings:  Optional[int]   = None     # Computed — count of active ratings
    is_active:      bool
    created_at:     datetime

    class Config:
        from_attributes = True


class NetaDetailResponse(NetaResponse):
    """
    Leader detail screen — includes whether the current user
    has already rated this neta in the active window.
    """
    has_rated_this_window: bool = False


# ─── Rating Window Schemas ───────────────────────────────────

class RatingWindowResponse(BaseModel):
    """Current window status — sent to Flutter to control UI state."""
    id:        str
    label:     str                  # "Jan 2025"
    opens_at:  datetime
    closes_at: datetime
    is_hidden: bool
    is_open:   bool                 # Computed: now is between opens_at and closes_at AND not hidden

    class Config:
        from_attributes = True


# ─── Rating Schemas ──────────────────────────────────────────

class NetaRatingCreate(BaseModel):
    """Verified user submits a rating during an open window."""
    stars: int

    @field_validator("stars")
    @classmethod
    def validate_stars(cls, v):
        if v < 1 or v > 5:
            raise ValueError("Stars must be between 1 and 5.")
        return v


class NetaRatingResponse(BaseModel):
    """Single rating response."""
    id:         str
    neta_id:    str
    window_id:  str
    rated_by:   str
    stars:      int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── History / Graph Schema ──────────────────────────────────

class RatingHistoryPoint(BaseModel):
    """
    One data point on the rating history graph.
    X-axis = cycle label, Y-axis = average stars.
    """
    window_label:   str     # "Jan 2024", "Jul 2024" etc.
    average_stars:  float
    total_ratings:  int
    window_closes:  datetime


class NetaHistoryResponse(BaseModel):
    """Full history for a neta — used to render the graph."""
    neta_id:   str
    neta_name: str
    history:   List[RatingHistoryPoint]