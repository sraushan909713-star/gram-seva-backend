# ============================================================
# app/models/otp.py — OTPs Table Definition
# ============================================================
# This file defines the 'otps' table — temporary one-time
# passwords sent to users during registration and login.
#
# IMPORTS FROM: app/database.py (Base — the parent class)
# IMPORTED BY:  app/routers/auth.py (to create and verify OTPs)
#
# Using an enum means only these exact values are allowed
# ============================================================

import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum

from app.database import Base


# Purpose tells us why this OTP was created.
# Same table handles both registration and login flows.
class OTPPurpose(str, enum.Enum):
    registration = "registration"
    login = "login"
    reset_password = "reset_password"


class OTP(Base):
    __tablename__ = "otps"

    # Unique ID for each OTP record.
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # The phone number this OTP was sent to.
    # We link by phone (not user ID) because during registration
    # the user doesn't have an ID yet — they're not created yet.
    phone = Column(String, nullable=False, index=True)

    # The actual 6-digit code. In V1 we store it as plain text.
    # In a future version this could be hashed for extra security.
    otp_code = Column(String, nullable=False)

    # Was this OTP created for registration or login?
    purpose = Column(Enum(OTPPurpose), nullable=False)

    # Once an OTP is used, this flips to True and it's dead —
    # even if it hasn't expired yet. Prevents reuse attacks.
    is_used = Column(Boolean, default=False, nullable=False)

    # OTP expires 10 minutes after creation.
    # Set by the router when creating the OTP — not auto-set here.
    expires_at = Column(DateTime, nullable=False)

    # When this OTP was created — useful for auditing and cleanup.
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
