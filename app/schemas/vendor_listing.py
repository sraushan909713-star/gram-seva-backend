# app/schemas/vendor_listing.py
# ─────────────────────────────────────────────────────────────
# Pydantic schemas for vendor listings API.
#
# VendorListingCreate  → vendor posts a new listing
# VendorListingUpdate  → vendor updates price/stock
# VendorListingResponse → what the app receives
# ─────────────────────────────────────────────────────────────

from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.vendor_listing import VendorCategory, StockStatus


# — REQUEST SCHEMAS ───────────────────────────────────────────

class VendorListingCreate(BaseModel):
    """
    Used when a Vendor creates a new product listing.
    vendor_id and vendor_name are taken from their JWT token — not sent manually.
    """
    product_name: str                           # "Paddy (Dhan)"
    product_name_hindi: Optional[str] = None   # "धान"
    category: VendorCategory                   # crops / animal_feed
    price: str                                 # "2100"
    unit: str                                  # "per quintal"
    stock_status: StockStatus = StockStatus.in_stock
    notes: Optional[str] = None
    village_id: str = "1"


class VendorListingUpdate(BaseModel):
    """
    Used when Vendor updates an existing listing.
    Most common use: update today's price and stock status.
    All fields optional — only send what changed.
    """
    product_name: Optional[str] = None
    product_name_hindi: Optional[str] = None
    category: Optional[VendorCategory] = None
    price: Optional[str] = None
    unit: Optional[str] = None
    stock_status: Optional[StockStatus] = None
    notes: Optional[str] = None


# — RESPONSE SCHEMA ───────────────────────────────────────────

class VendorListingResponse(BaseModel):
    """
    Returned by the API in every vendor listing response.
    Flutter app uses updated_at to show "last updated X hours ago".
    """
    id: str
    village_id: str
    vendor_id: str
    vendor_name: str
    product_name: str
    product_name_hindi: Optional[str]
    category: VendorCategory
    price: str
    unit: str
    stock_status: StockStatus
    notes: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True