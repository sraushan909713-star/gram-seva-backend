# ============================================================
# main.py — Application Entry Point
# ============================================================
# This is the first file FastAPI reads when the server starts.
# It creates the FastAPI app instance and registers everything:
# routers, middleware, startup events, etc.
#
# Think of this as the front door of your entire backend.
# Every API request enters through here.
# ============================================================

from fastapi import FastAPI
from app.database import engine, Base

# This creates all database tables automatically on startup.
# SQLAlchemy looks at all models that inherit from Base and
# creates their tables if they don't already exist.
# Safe to run multiple times — it skips existing tables.
Base.metadata.create_all(bind=engine)

# Create the FastAPI app instance.
# title and version appear in the auto-generated API docs.
app = FastAPI(
    title="Gram Seva API",
    version="1.0.0",
    description="Backend API for Gram Seva — Jagruk Durbe"
)


# A simple health check endpoint.
# Visit http://127.0.0.1:8000/ in your browser to confirm
# the server is running. Returns a JSON response.
@app.get("/")
def root():
    return {"message": "Gram Seva API is running 🏡"}