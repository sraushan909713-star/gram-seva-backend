# app/routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.otp import create_otp, verify_otp
from app.core.security import hash_password, create_access_token, verify_password
from app.models.otp import OTPPurpose   # ✅ your enum
from app.models.user import User, UserRole
from app.schemas.auth import SendOTPRequest, RegisterRequest, TokenResponse, LoginRequest, ResetPasswordRequest

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/send-otp")
def send_otp(request: SendOTPRequest, db: Session = Depends(get_db)):
    """Send OTP to phone. Returns code in response (dev only)."""
    purpose = OTPPurpose(request.purpose)  # converts "registration" string → enum
    code = create_otp(db, phone=request.phone, purpose=purpose)

    # TODO: replace with real SMS gateway in production
    return {
        "message": f"OTP sent to {request.phone}",
        "otp": code  # ⚠️ REMOVE IN PRODUCTION
    }


@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Verify OTP + create user account + return JWT token."""

    # 1. Verify OTP
    otp_valid = verify_otp(
        db,
        phone=request.phone,
        code=request.otp_code,
        purpose=OTPPurpose.registration  # ✅ using your enum value
    )
    if not otp_valid:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    # 2. Check phone not already registered
    existing = db.query(User).filter(User.phone == request.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone already registered")

    # 3. Create user
    new_user = User(
        phone=request.phone,
        full_name=request.name,
        display_name=request.name,
        password_hash=hash_password(request.password),
        role=UserRole.user,
        village_id=1,  
        is_durbe_resident=False,
        is_verified=False,
        is_active=True,     # Durbe = village 1
        badge="pending",    # Admin must verify to become "Durbe Niwasi"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # 4. Issue JWT
    token = create_access_token(data={
        "sub": str(new_user.id),
        "role": new_user.role,
        "badge": new_user.badge,
    })

    return {"access_token": token, "token_type": "bearer"}


@router.post("/login", response_model=TokenResponse)  # ✅ ADD FROM HERE
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with phone + password.
    No OTP needed — user already verified their phone during registration.
    """
    # 1. Find user by phone
    user = db.query(User).filter(User.phone == request.phone).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No account found with this phone number"
        )

    # 2. Check password matches stored hash
    if not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )

    # 3. Check account is active (not banned)
    if not user.is_active:
        raise HTTPException(
            status_code=400,
            detail="Your account has been deactivated. Contact admin."
        )

    # 4. Issue JWT — same structure as registration token
    token = create_access_token(data={
        "sub": str(user.id),
        "role": user.role.value,  # .value converts enum → string e.g. "user"
        "badge": user.badge,
    })

    return {"access_token": token, "token_type": "bearer"}  # ✅ ADD UNTIL HERE


@router.post("/reset-password", response_model=TokenResponse) 
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Reset forgotten password using OTP verification.
    User must first call /send-otp with purpose="reset_password".
    Returns a JWT so user is logged in immediately after reset.
    """
    # 1. Check user exists
    user = db.query(User).filter(User.phone == request.phone).first()
    if not user:
        raise HTTPException(
            status_code=400,
            detail="No account found with this phone number"
        )

    # 2. Verify OTP (purpose must be reset_password, not registration)
    otp_valid = verify_otp(
        db,
        phone=request.phone,
        code=request.otp_code,
        purpose=OTPPurpose.reset_password  # ✅ uses the new enum value we added
    )
    if not otp_valid:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired OTP"
        )

    # 3. Update password — hash the new one before saving
    user.password_hash = hash_password(request.new_password)
    db.commit()

    # 4. Issue fresh JWT — user is logged in immediately after reset
    token = create_access_token(data={
        "sub": str(user.id),
        "role": user.role.value,
        "badge": user.badge,
    })

    return {"access_token": token, "token_type": "bearer"}
