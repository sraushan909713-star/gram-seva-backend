# app/schemas/weather.py
# ─────────────────────────────────────────────
# These are Pydantic schemas for the Rain Alert feature.
# Schemas define the SHAPE of data we send back to the Flutter app.
# No database involved here — this is purely for API response structure.
# ─────────────────────────────────────────────

from pydantic import BaseModel
from typing import List
from datetime import date, datetime


class DailyForecast(BaseModel):
    """
    Represents one day's rainfall forecast.
    The Flutter app will use this to show a 7-day forecast list.
    """
    date: date                  # e.g. 2026-04-01
    rainfall_mm: float          # total rainfall expected that day in millimetres
    warning_level: str          # "None", "Low", or "Heavy"
    temp_max_c: float       # ✅ ADD: daily max temperature in Celsius
    temp_min_c: float      # ✅ ADD: daily min temperature in Celsius


class RainAlertResponse(BaseModel):
    """
    The full response returned by GET /weather/rain-alert.
    Flutter will parse this and render the rain alert screen.
    """
    location: str               # Always "Durbe, Bihar" in V1
    today_rainfall_mm: float    # Today's total rainfall in mm
    today_temp_max_c: float     # ✅ ADD: today's max temperature
    today_temp_min_c: float     # ✅ ADD: today's min temperature
    warning_level: str          # Today's warning: "None", "Low", or "Heavy"
    forecast: List[DailyForecast]  # 7-day forecast list
    last_updated: datetime      # When this data was fetched from Open-Meteo
    current_temp_c: float     # ✅ ADD: current temperature from Open-Meteo's current_weather
