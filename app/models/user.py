# ============================================================
# app/models/user.py — Users Table Definition
# ============================================================
# This file defines the structure of the 'users' table in
# the database. Every column we designed is defined here
# as a Python class attribute using SQLAlchemy.
#
# IMPORTS FROM: app/database.py (Base — the parent class)
# IMPORTED BY:  app/main.py (so table gets created on startup)
#               app/routers/auth.py (to query/create users)
#
# MENTAL MODEL:
#   This class = one table in the database
#   Each attribute = one column in that table
#   Each row in the table = one User object in Python
# ============================================================

import uuid
from sqlalchemy import Column, String, Boolean, Integer, DateTime, Enum
from sqlalchemy.sql import func
import enum

from app.database import Base


# Python enum for user roles.
# Using an enum means only these exact values are allowed —
# no typos like "Admin" or "ADMIN" can sneak into the database.
class UserRole(str, enum.Enum):
    super_admin = "super_admin"
    admin = "admin"
    vendor = "vendor"
    user = "user"


class User(Base):
    __tablename__ = "users"

    # Primary key — unique ID for every user.
    # We generate a UUID in Python (not the database) so it
    # works consistently across SQLite and PostgreSQL.
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    # Village this user belongs to.
    # Hardcoded to 1 (Durbe) for now. The column exists so
    # future multi-village expansion needs no schema change.
    village_id = Column(Integer, default=1, nullable=False)

    full_name = Column(String, nullable=False)

    display_name = Column(String, nullable=False)

    phone = Column(String, unique=True, nullable=False, index=True)

    password_hash = Column(String, nullable=False)

    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)

    profile_photo_url = Column(String, nullable=True)

    is_durbe_resident = Column(Boolean, default=False, nullable=False)

    is_verified = Column(Boolean, default=False, nullable=False)

    badge = Column(String, default="none", nullable=False)

    verified_by = Column(String, nullable=True)

    verified_at = Column(DateTime, nullable=True)

    # Is this account active? False = banned by admin.
    # We never delete users — we just deactivate them.
    # This preserves data integrity (their posts, votes etc. remain).
    is_active = Column(Boolean, default=True, nullable=False)

    # Automatically set to current time when the user registers.
    # server_default=func.now() lets the database set this value.
    created_at = Column(DateTime, server_default=func.now(), nullable=False)