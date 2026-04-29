# app/routers/guides.py
# ─────────────────────────────────────────────────────────────
# API endpoints for the Documentation Guides feature.
#
# PUBLIC (no login needed):
#   GET  /guides/          → list all guides (optional filter by category)
#   GET  /guides/{id}      → get one guide's full step-by-step details
#
# ADMIN ONLY (JWT token required, role must be admin or super_admin):
#   POST   /guides/        → add a new guide
#   PUT    /guides/{id}    → edit an existing guide
#   DELETE /guides/{id}    → soft delete (hides from app, stays in database)
# ─────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.guide import Guide, GuideCategory
from app.models.user import User
from app.schemas.guide import GuideCreate, GuideUpdate, GuideResponse, GuideListResponse
from app.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/guides",
    tags=["Documentation Guides"]
)

# ─────────────────────────────────────────────────────────────
# Bearer token scheme for Swagger UI
# ─────────────────────────────────────────────────────────────

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
bearer_scheme = HTTPBearer()


# ─────────────────────────────────────────────────────────────
# HELPER: Get the currently logged-in user from JWT token
# ─────────────────────────────────────────────────────────────

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Decodes the JWT token from the request header.
    Returns the User object if token is valid.
    Raises 401 if token is missing or invalid.
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
# HELPER: Verify the user is Admin or Super Admin
# ─────────────────────────────────────────────────────────────

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """
    Checks if the logged-in user has admin or super_admin role.
    Raises 403 Forbidden if they don't.
    Regular villagers cannot add/edit/delete guides.
    """
    if current_user.role not in ("admin", "super_admin"):
        raise HTTPException(
            status_code=403,
            detail="Access denied. Only Admins can manage guides."
        )
    return current_user


# ─────────────────────────────────────────────────────────────
# PUBLIC ENDPOINTS (no login required)
# ─────────────────────────────────────────────────────────────

@router.get("/", response_model=List[GuideListResponse])
def get_all_guides(
    category: Optional[GuideCategory] = Query(None, description="Filter: certificate / welfare / land / education / health / other"),
    village_id: str = Query("1"),
    db: Session = Depends(get_db)
):
    """
    Returns all active guides for a village.
    Optionally filter by category.
    Returns lightweight list view — no steps or tips to keep it fast.
    No login required — any villager can browse guides.
    """
    query = db.query(Guide).filter(
        Guide.is_active == True,
        Guide.village_id == village_id
    )

    if category:
        query = query.filter(Guide.category == category)

    return query.order_by(Guide.category, Guide.title).all()


@router.get("/{guide_id}", response_model=GuideResponse)
def get_guide(guide_id: str, db: Session = Depends(get_db)):
    """
    Returns full details of a single guide by ID.
    Includes steps, documents needed, office info, and Admin tips.
    No login required — any villager can view.
    """
    guide = db.query(Guide).filter(
        Guide.id == guide_id,
        Guide.is_active == True
    ).first()

    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found.")

    return guide


# ─────────────────────────────────────────────────────────────
# ADMIN ENDPOINTS (JWT token required, Admin or Super Admin only)
# ─────────────────────────────────────────────────────────────

@router.post("/", response_model=GuideResponse)
def create_guide(
    data: GuideCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Admin adds a new documentation guide.
    Admin must have visited the office first to get accurate information.
    """
    guide = Guide(**data.model_dump())
    db.add(guide)
    db.commit()
    db.refresh(guide)
    return guide


@router.put("/{guide_id}", response_model=GuideResponse)
def update_guide(
    guide_id: str,
    data: GuideUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Updates an existing guide.
    Only Admins and Super Admins can do this.
    Only the fields that are sent will be updated — others stay unchanged.
    """
    guide = db.query(Guide).filter(
        Guide.id == guide_id,
        Guide.is_active == True
    ).first()

    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found.")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(guide, field, value)

    db.commit()
    db.refresh(guide)
    return guide


@router.delete("/{guide_id}")
def delete_guide(
    guide_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Soft deletes a guide — sets is_active = False.
    The guide stays in the database but disappears from the app.
    Only Admins and Super Admins can do this.
    """
    guide = db.query(Guide).filter(
        Guide.id == guide_id,
        Guide.is_active == True
    ).first()

    if not guide:
        raise HTTPException(status_code=404, detail="Guide not found.")

    guide.is_active = False
    db.commit()
    return {"message": f"Guide '{guide.title}' deleted successfully."}