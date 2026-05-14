# app/models/banner.py
# ─────────────────────────────────────────────────────────────
# Home Screen Banners — auto-scrolling carousel on home tab.
#
# Two banner types supported:
#   Image banner  → image_url is set (Cloudinary URL)
#   Color banner  → bg_color_start + bg_color_end (hex gradient)
#
# If image_url is set → show image with title overlay
# If no image → show color gradient with icon + title + subtitle
#
# Managed by Super Admin only via Swagger.
# Weather slide is hardcoded in Flutter — not stored here.
# ─────────────────────────────────────────────────────────────

import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from app.database import Base


class Banner(Base):
    __tablename__ = "banners"

    # ── Identity ──────────────────────────────────────────────
    id         = Column(String, primary_key=True,
                        default=lambda: str(uuid.uuid4()))
    village_id = Column(String, nullable=False, default="1")

    # ── Content ───────────────────────────────────────────────
    title    = Column(String, nullable=False)      # Overlay text on banner
    subtitle = Column(String, nullable=True)       # Optional second line
    icon     = Column(String, nullable=True)       # Emoji e.g. "💼" (color banners only)

    # ── Image banner ──────────────────────────────────────────
    # If set → show this image. Cloudinary URL.
    image_url = Column(String, nullable=True)

    # ── Color gradient banner ─────────────────────────────────
    # Used when image_url is None
    bg_color_start = Column(String, nullable=True)  # Hex e.g. "#1E3A5F"
    bg_color_end   = Column(String, nullable=True)  # Hex e.g. "#166534"

    # ── Redirect ──────────────────────────────────────────────
    # redirect_type: "internal" or "external" or None
    # redirect_target:
    #   internal → screen name e.g. "job_alerts", "gram_awaaz",
    #              "neta_report_card", "rain_alerts", "vikas_prastav"
    #   external → full URL e.g. "https://ssc.nic.in"
    redirect_type   = Column(String, nullable=True)
    redirect_target = Column(String, nullable=True)

    # ── Display ───────────────────────────────────────────────
    display_order = Column(Integer, default=0, nullable=False)
    # Tag shown in top-right corner e.g. "Job Alert", "Weather", "Gram Sabha"
    tag           = Column(String, nullable=True)

    # ── Auto-expiry ───────────────────────────────────────────
    # Banner auto-hides after this date. Null = never expires.
    valid_until = Column(DateTime(timezone=True), nullable=True)

    # ── Visibility ────────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)

    # ── Timestamps ────────────────────────────────────────────
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())