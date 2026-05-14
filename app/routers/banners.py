# app/routers/banners.py
# ─────────────────────────────────────────────────────────────
# Home Screen Banners API
#
# PUBLIC:
#   GET  /banners/          → active, non-expired banners for Flutter
#
# SUPER ADMIN ONLY:
#   POST   /banners/        → add a new banner
#   PATCH  /banners/{id}    → edit a banner
#   DELETE /banners/{id}    → soft delete
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List

from app.database import get_db
from app.models.banner import Banner
from app.models.user import User
from app.schemas.banner import BannerCreate, BannerUpdate, BannerResponse
from app.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/banners", tags=["Banners"])
bearer_scheme = HTTPBearer()


# ─── Helpers ─────────────────────────────────────────────────

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token.")
    user = db.query(User).filter(User.id == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found.")
    return user


def require_super_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=403,
            detail="Super Admin access required to manage banners."
        )
    return current_user


# ─── Public ──────────────────────────────────────────────────

@router.get("/", response_model=List[BannerResponse])
def get_active_banners(db: Session = Depends(get_db)):
    """
    Returns all active, non-expired banners sorted by display_order.
    Flutter calls this on home screen load.
    Auto-filters out banners past their valid_until date.
    No login required.
    """
    now = datetime.utcnow()
    banners = db.query(Banner).filter(
        Banner.is_active == True,
    ).order_by(Banner.display_order.asc()).all()

    # ── Filter out expired banners ────────────────────────────
    active = []
    for b in banners:
        if b.valid_until is None:
            active.append(b)
        elif b.valid_until.replace(tzinfo=None) > now:
            active.append(b)

    return active


# ─── Super Admin ─────────────────────────────────────────────

@router.post("/", response_model=BannerResponse, status_code=201)
def create_banner(
    data: BannerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Super Admin adds a new banner."""
    banner = Banner(**data.model_dump())
    db.add(banner)
    db.commit()
    db.refresh(banner)
    return banner


@router.patch("/{banner_id}", response_model=BannerResponse)
def update_banner(
    banner_id: str,
    data: BannerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Super Admin edits a banner."""
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found.")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(banner, field, value)
    db.commit()
    db.refresh(banner)
    return banner


@router.delete("/{banner_id}", status_code=200)
def delete_banner(
    banner_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_super_admin)
):
    """Soft deletes a banner."""
    banner = db.query(Banner).filter(Banner.id == banner_id).first()
    if not banner:
        raise HTTPException(status_code=404, detail="Banner not found.")
    banner.is_active = False
    db.commit()
    return {"message": "Banner removed successfully."}