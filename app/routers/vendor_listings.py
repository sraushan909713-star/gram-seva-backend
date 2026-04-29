# app/routers/vendor_listings.py
# ─────────────────────────────────────────────────────────────
# API endpoints for Vendor Listings (Mandi Prices feature).
#
# PUBLIC (no login):
#   GET  /vendor-listings/       → all active listings
#   GET  /vendor-listings/{id}   → single listing
#
# VENDOR ONLY (must have role=vendor):
#   POST   /vendor-listings/     → create new listing
#   PUT    /vendor-listings/{id} → update price/stock
#   DELETE /vendor-listings/{id} → soft delete own listing
#
# ADMIN can also DELETE any listing if needed.
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.vendor_listing import VendorListing, VendorCategory
from app.models.user import User, UserRole
from app.schemas.vendor_listing import (
    VendorListingCreate, VendorListingUpdate, VendorListingResponse
)
from app.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/vendor-listings",
    tags=["Vendor Listings — Mandi Prices"]
)

# ─────────────────────────────────────────────────────────────
# Bearer token scheme for Swagger UI
# ─────────────────────────────────────────────────────────────

bearer_scheme = HTTPBearer()


# ─────────────────────────────────────────────────────────────
# HELPER: Get the currently logged-in user from JWT token
# ─────────────────────────────────────────────────────────────

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Decodes JWT token and returns the logged-in User.
    Raises 401 if token is invalid or expired.
    """
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user


# ─────────────────────────────────────────────────────────────
# HELPER: Only vendors and admins can manage listings
# ─────────────────────────────────────────────────────────────

def require_vendor(current_user: User = Depends(get_current_user)) -> User:
    """
    Only users with role=vendor, admin, or super_admin can create/edit listings.
    Regular villagers (role=user) can only view.
    """
    if current_user.role not in [UserRole.vendor, UserRole.admin, UserRole.super_admin]:
        raise HTTPException(
            status_code=403,
            detail="Only vendors can manage listings."
        )
    return current_user


# ─────────────────────────────────────────────────────────────
# PUBLIC ENDPOINTS (no login required)
# ─────────────────────────────────────────────────────────────

@router.get("/", response_model=List[VendorListingResponse])
def get_all_listings(
    category: Optional[VendorCategory] = Query(None, description="Filter: crops / animal_feed"),
    village_id: str = Query("1"),
    db: Session = Depends(get_db)
):
    """
    Returns all active vendor listings for a village.
    Villagers use this to check today's mandi prices.
    Sorted by most recently updated — freshest prices first.
    No login required.
    """
    query = db.query(VendorListing).filter(
        VendorListing.is_active == True,
        VendorListing.village_id == village_id
    )

    if category:
        query = query.filter(VendorListing.category == category)

    # ✅ Most recently updated first — so fresh prices appear at top
    return query.order_by(VendorListing.updated_at.desc()).all()


@router.get("/{listing_id}", response_model=VendorListingResponse)
def get_listing(listing_id: str, db: Session = Depends(get_db)):
    """
    Returns full details of a single vendor listing.
    No login required.
    """
    listing = db.query(VendorListing).filter(
        VendorListing.id == listing_id,
        VendorListing.is_active == True
    ).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")
    return listing


# ─────────────────────────────────────────────────────────────
# VENDOR ENDPOINTS (JWT required, role=vendor/admin)
# ─────────────────────────────────────────────────────────────

@router.post("/", response_model=VendorListingResponse)
def create_listing(
    data: VendorListingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_vendor)
):
    """
    Vendor creates a new product listing.
    vendor_id and vendor_name are auto-filled from their JWT token.
    """
    listing = VendorListing(
        **data.model_dump(),
        vendor_id=current_user.id,
        vendor_name=current_user.full_name,  # auto from token
    )
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.put("/{listing_id}", response_model=VendorListingResponse)
def update_listing(
    listing_id: str,
    data: VendorListingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_vendor)
):
    """
    Vendor updates their listing — most commonly to change today's price.
    Vendors can only edit their OWN listings.
    Admins can edit any listing.
    """
    listing = db.query(VendorListing).filter(
        VendorListing.id == listing_id,
        VendorListing.is_active == True
    ).first()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")

    # ✅ Vendors can only edit their own listings
    if current_user.role == UserRole.vendor and listing.vendor_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only edit your own listings."
        )

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(listing, field, value)

    db.commit()
    db.refresh(listing)
    return listing


@router.delete("/{listing_id}")
def delete_listing(
    listing_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_vendor)
):
    """
    Soft deletes a listing.
    Vendors can only delete their own. Admins can delete any.
    """
    listing = db.query(VendorListing).filter(
        VendorListing.id == listing_id,
        VendorListing.is_active == True
    ).first()

    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found.")

    if current_user.role == UserRole.vendor and listing.vendor_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You can only delete your own listings."
        )

    listing.is_active = False
    db.commit()
    return {"message": f"Listing '{listing.product_name}' deleted successfully."}
