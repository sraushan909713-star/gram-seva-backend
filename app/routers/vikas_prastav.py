# app/routers/vikas_prastav.py
# ─────────────────────────────────────────────
# Vikas Prastav — Development Proposals
# Villagers propose development projects with community upvote support.
# Anyone can read. Any logged-in user can post or upvote.
# ─────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.vikas_prastav import VikasPrastav, VikasPrastavUpvote, ProposalCategory
from app.models.user import User
from app.schemas.vikas_prastav import (
    VikasPrastavCreate, VikasPrastavResponse,
    VikasPrastavListResponse, UpvoteResponse
)
from app.core.security import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(
    prefix="/vikas-prastav",
    tags=["Vikas Prastav"]
)

bearer_scheme = HTTPBearer()


# ─────────────────────────────────────────────
# HELPER: Get current logged-in user
# ─────────────────────────────────────────────
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


# ─────────────────────────────────────────────
# HELPER: Admin check
# ─────────────────────────────────────────────
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role not in ("admin", "super_admin"):
        raise HTTPException(status_code=403, detail="Access denied.")
    return current_user


# ─────────────────────────────────────────────
# PUBLIC ENDPOINTS
# ─────────────────────────────────────────────

@router.get("", response_model=List[VikasPrastavListResponse])
def list_proposals(
    category: Optional[ProposalCategory] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """
    Returns all active development proposals.
    Sorted by upvote count — most supported proposals appear first.
    No login required — anyone can read proposals.
    """
    query = db.query(VikasPrastav).filter(VikasPrastav.is_active == True)

    if category:
        query = query.filter(VikasPrastav.category == category)

    # ✅ Most upvoted first — highest community mandate rises to top
    return query.order_by(VikasPrastav.upvote_count.desc()).all()


@router.get("/{proposal_id}", response_model=VikasPrastavResponse)
def get_proposal(proposal_id: str, db: Session = Depends(get_db)):
    """
    Returns full details of a single proposal.
    No login required.
    """
    proposal = db.query(VikasPrastav).filter(
        VikasPrastav.id == proposal_id,
        VikasPrastav.is_active == True
    ).first()

    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found.")

    return proposal


# ─────────────────────────────────────────────
# LOGGED-IN USER ENDPOINTS
# ─────────────────────────────────────────────

@router.post("", response_model=VikasPrastavResponse, status_code=201)
def create_proposal(
    data: VikasPrastavCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submits a new development proposal.
    Any logged-in user can propose.
    Photo is mandatory — show the current condition that needs improvement.
    """
    proposal = VikasPrastav(
        title=data.title,
        description=data.description,
        location=data.location,
        category=data.category,
        photo_url_1=data.photo_url_1,   # ✅ CHANGE
        photo_url_2=data.photo_url_2,   # ✅ ADD
        photo_url_3=data.photo_url_3,   # ✅ ADD
        photo_url_4=data.photo_url_4,   # ✅ ADD
        estimated_cost=data.estimated_cost,
        funding_source=data.funding_source,
        posted_by=current_user.id
    )
    db.add(proposal)
    db.commit()
    db.refresh(proposal)
    return proposal


@router.post("/{proposal_id}/upvote", response_model=UpvoteResponse)
def upvote_proposal(
    proposal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upvotes a development proposal.
    Each user can only upvote a proposal once.
    Upvote count = community mandate for this development.
    """
    proposal = db.query(VikasPrastav).filter(
        VikasPrastav.id == proposal_id,
        VikasPrastav.is_active == True
    ).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found.")

    # Check if user already upvoted
    existing = db.query(VikasPrastavUpvote).filter(
        VikasPrastavUpvote.post_id == proposal_id,
        VikasPrastavUpvote.user_id == current_user.id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="You have already upvoted this proposal."
        )

    # Record the upvote
    upvote = VikasPrastavUpvote(
        post_id=proposal_id,
        user_id=current_user.id
    )
    db.add(upvote)
    proposal.upvote_count += 1
    db.commit()

    return UpvoteResponse(
        message="Upvote recorded successfully.",
        upvote_count=proposal.upvote_count
    )


# ─────────────────────────────────────────────
# ADMIN-ONLY ENDPOINTS
# ─────────────────────────────────────────────

@router.delete("/{proposal_id}", status_code=200)
def delete_proposal(
    proposal_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Soft-deletes a proposal — only Admin or Super Admin can do this.
    """
    proposal = db.query(VikasPrastav).filter(
        VikasPrastav.id == proposal_id
    ).first()
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found.")

    proposal.is_active = False
    db.commit()
    return {"message": "Proposal removed successfully."}