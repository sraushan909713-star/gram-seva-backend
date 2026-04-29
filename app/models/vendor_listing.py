# app/models/vendor_listing.py
# ─────────────────────────────────────────────────────────────
# Defines the "vendor_listings" table.
# Vendors (role=vendor) post their crop/animal feed prices here.
# Admin creates vendor accounts. Vendors log in and update prices.
# Villagers see live prices without travelling to the mandi.
# ─────────────────────────────────────────────────────────────

import uuid
import enum
from sqlalchemy import Column, String, Boolean, DateTime, Enum, Text, ForeignKey
from sqlalchemy.sql import func
from app.database import Base


class VendorCategory(str, enum.Enum):
    """
    What type of product is this vendor selling?
    """
    crops       = "crops"        # Paddy, wheat, mustard, maize
    animal_feed = "animal_feed"  # Cattle feed, poultry feed, khali


class StockStatus(str, enum.Enum):
    """
    Is this product currently available?
    """
    in_stock    = "in_stock"
    limited     = "limited"
    out_of_stock = "out_of_stock"


class VendorListing(Base):
    __tablename__ = "vendor_listings"

    # — Identity ──────────────────────────────────────────────
    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    # — Village tag ───────────────────────────────────────────
    village_id = Column(String, nullable=False, default="1")

    # — Vendor who posted this listing ────────────────────────
    # Links to the users table — vendor must have role=vendor
    vendor_id = Column(String, nullable=False)      # FK to users.id
    vendor_name = Column(String, nullable=False)    # Denormalized for fast display

    # — Product details ───────────────────────────────────────
    product_name = Column(String, nullable=False)   # "Paddy (Dhan)", "Cattle Feed (Khali)"
    product_name_hindi = Column(String, nullable=True)  # "धान", "खली"
    category = Column(Enum(VendorCategory), nullable=False)

    # — Pricing ───────────────────────────────────────────────
    price = Column(String, nullable=False)          # "2100" — stored as string for flexibility
    unit = Column(String, nullable=False)           # "per quintal", "per kg", "per bag"

    # — Stock status ──────────────────────────────────────────
    stock_status = Column(
        Enum(StockStatus),
        nullable=False,
        default=StockStatus.in_stock
    )

    # — Extra info ────────────────────────────────────────────
    notes = Column(Text, nullable=True)  # e.g. "Fresh harvest, quality A grade"

    # — Soft delete ───────────────────────────────────────────
    is_active = Column(Boolean, default=True, nullable=False)

    # — Timestamps ────────────────────────────────────────────
    # created_at = when listing was first created
    # updated_at = when vendor last updated price — shown as "last updated"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())