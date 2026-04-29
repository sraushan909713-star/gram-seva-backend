# app/schemas/auth.py — Pydantic Models for Authentication

from pydantic import BaseModel

class SendOTPRequest(BaseModel):
    phone: str
    purpose: str  # "registration" or "login"

class RegisterRequest(BaseModel):
    phone: str
    name: str
    otp_code: str   # 6-digit code the user received
    password: str   # will be hashed before saving

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):  # ✅ ADD THIS — new class for login
    phone: str
    password: str  # plain text — we'll verify against stored hash

class ResetPasswordRequest(BaseModel):  # ✅ ADD THIS — new class for password reset
    phone: str
    otp_code: str       # OTP sent with purpose="reset_password"
    new_password: str   # will be hashed before saving
