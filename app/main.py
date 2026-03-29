# ============================================================
# main.py — Application Entry Point
# ============================================================
# This is the first file FastAPI reads when the server starts.
# It creates the FastAPI app instance and registers everything.
#
# IMPORTS FROM: app/database.py (engine, Base)
#               app/models/user.py (User table)
#               app/models/otp.py  (OTP table)
# IMPORTED BY:  nothing — this is the top of the chain
#
# STARTUP SEQUENCE:
#   1. Models are imported → they register themselves with Base
#   2. create_all() sees all registered models → creates tables
#   3. FastAPI app is created
#   4. Routers are registered (we'll add these soon)
#   5. Server starts listening for requests
# ============================================================

from fastapi import FastAPI
from app.database import engine, Base

# Importing models so SQLAlchemy knows they exist before
# create_all() runs. Without these imports, the tables
# would never be created — Base wouldn't know about them.
from app.models import user, otp

# Create all tables that are registered with Base.
# Safe to run every startup — skips tables that already exist.
Base.metadata.create_all(bind=engine)

# Create the FastAPI app instance.
app = FastAPI(
    title="Gram Seva API",
    version="1.0.0",
    description="Backend API for Gram Seva — Jagruk Durbe"
)

# Health check endpoint — confirms the server is running.
@app.get("/")
def root():
    return {"message": "Gram Seva API is running 🏡"}