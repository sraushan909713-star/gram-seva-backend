# app/routers/weather.py
# ─────────────────────────────────────────────
# This router handles all weather-related endpoints.
# It calls the Open-Meteo API (free, no API key needed)
# and returns clean rainfall data for Durbe village.
# ─────────────────────────────────────────────

import httpx                          # For making HTTP calls to Open-Meteo API
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.schemas.weather import RainAlertResponse, DailyForecast

router = APIRouter(
    prefix="/weather",                # All endpoints here start with /weather
    tags=["Weather"]                  # Groups endpoints in Swagger UI
)

# ─────────────────────────────────────────────
# Durbe village coordinates (confirmed from Google Maps)
# These are hardcoded for V1 since we only serve one village
# ─────────────────────────────────────────────
DURBE_LAT = 24.8091356061036
DURBE_LON = 84.95446429007396
DURBE_LOCATION_NAME = "Durbe, Bihar"

# ─────────────────────────────────────────────
# IMD (India Meteorological Department) rainfall warning thresholds
# Using official Indian standards for accuracy
# ─────────────────────────────────────────────
def get_warning_level(rainfall_mm: float) -> str:
    """
    Converts a rainfall amount (mm) into a human-readable warning level.
    Thresholds follow IMD standards used across India.
    """
    if rainfall_mm <= 2.5:
        return "None"
    elif rainfall_mm <= 15:
        return "Low"
    else:
        return "Heavy"


@router.get("/rain-alert", response_model=RainAlertResponse)
async def get_rain_alert():
    """
    Fetches live rainfall data for Durbe village from Open-Meteo API.
    No login required — any villager can check rain status.
    Returns today's rainfall, warning level, and 7-day forecast.
    """

    # Open-Meteo API URL — free, no API key, highly accurate for India
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={DURBE_LAT}"
        f"&longitude={DURBE_LON}"
        f"&current_weather=true"
        f"&hourly=temperature_2m"
        f"&daily=precipitation_sum,temperature_2m_max,temperature_2m_min"
        f"&timezone=Asia%2FKolkata"
        f"&forecast_days=7"
    )

    try:
        # Make the API call to Open-Meteo
        # timeout=10 means we wait max 10 seconds before giving up
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=10)
            response.raise_for_status()  # Raises error if API returns 4xx/5xx
            data = response.json()

            print("FULL DATA:", data)  # 👈 ADD THIS
            print("CURRENT WEATHER:", data.get("current_weather"))  # 👈 ADD THIS

            current_temp = data.get("current_weather", {}).get("temperature", None)

    except httpx.TimeoutException:
        # Open-Meteo didn't respond in time
        raise HTTPException(status_code=504, detail="Weather service timed out. Please try again.")

    except httpx.HTTPError:
        # Open-Meteo returned an error response
        raise HTTPException(status_code=502, detail="Weather service unavailable. Please try again later.")

    # ─────────────────────────────────────────────
    # Parse the Open-Meteo response
    # data["daily"]["time"] → list of date strings ["2026-03-31", "2026-04-01", ...]
    # data["daily"]["precipitation_sum"] → list of mm values [0.0, 12.5, ...]
    # ─────────────────────────────────────────────
    daily_dates = data["daily"]["time"]
    daily_rainfall = data["daily"]["precipitation_sum"]
    daily_temp_max = data["daily"]["temperature_2m_max"]
    daily_temp_min = data["daily"]["temperature_2m_min"]

    # Build the 7-day forecast list
    forecast = []
    for i in range(len(daily_dates)):
        rainfall = daily_rainfall[i] or 0.0  # Replace None with 0.0
        forecast.append(DailyForecast(
            date=daily_dates[i],
            rainfall_mm=rainfall,
            warning_level=get_warning_level(rainfall),
            temp_max_c=daily_temp_max[i] or 0.0,
            temp_min_c=daily_temp_min[i] or 0.0
        ))

    # Today is always the first item in the forecast list
    today_rainfall = forecast[0].rainfall_mm
    today_warning = forecast[0].warning_level

    return RainAlertResponse(
        location=DURBE_LOCATION_NAME,
        today_rainfall_mm=today_rainfall,
        today_temp_max_c=forecast[0].temp_max_c,
        today_temp_min_c=forecast[0].temp_min_c,
        current_temp_c=current_temp,
        warning_level=today_warning,
        forecast=forecast,
        last_updated=datetime.now()
    )