# ============================================================
# database.py — Database Connection Setup
# ============================================================
# This file is responsible for one thing only:
# connecting our FastAPI app to the database.
#
# We are using SQLAlchemy — a library that lets us talk to
# the database using Python code instead of raw SQL queries.
#
# FLOW:
#   .env file → DATABASE_URL → engine → SessionLocal → get_db()
#   (config)     (address)    (driver)  (conversations) (injector)
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# load_dotenv() reads our .env file and makes its values
# available via os.getenv(). This keeps secrets out of code.
load_dotenv()

# DATABASE_URL is the full address of our database.
# Format: "sqlite:///./gramseva.db" for development (SQLite)
# Later in production this will point to PostgreSQL on Railway.
DATABASE_URL = os.getenv("DATABASE_URL")

# The engine is the actual connection to the database.
# Think of it as the pipe between Python and the database.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory that creates database sessions.
# A session = one conversation with the database (open, query, close).
# autocommit=False → we control when changes are saved
# autoflush=False  → changes aren't sent until we say so
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the foundation class for all our database models.
# Every table we create (users, otps, etc.) will inherit from Base.
# SQLAlchemy uses Base to track and create all our tables.
Base = declarative_base()


# get_db() is a dependency — FastAPI will call this automatically
# whenever an API endpoint needs to talk to the database.
# It opens a session, gives it to the endpoint, then closes it.
# The try/finally ensures the session ALWAYS closes, even if
# an error occurs mid-request. No leaked connections.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
