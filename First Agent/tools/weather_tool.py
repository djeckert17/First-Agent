"""
Weather Tool for Marbella Travel Agent
Fetches weather forecasts from yr.no API for any location.
"""

import aiohttp
from typing import Any
from claude_agent_sdk import tool


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit."""
    return (celsius * 9 / 5) + 32


def format_temperature(celsius: float, units: str = "fahrenheit") -> str:
    """Format temperature with proper units."""
    if units.lower() == "celsius":
        return f"{celsius:.1f}°C"
    else:
        fahrenheit = celsius_to_fahrenheit(celsius)
        return f"{fahrenheit:.1f}°F ({celsius:.1f}°C)"


@tool(
    "get_weather_forecast",
    "Get weather forecast for any location using latitude and longitude. Returns current conditions and 3-day forecast.",
    {
        "latitude": float,
        "longitude": float,
        "altitude": int,
        "location_name": str,
        "units": str
    }
)
async def get_weather_forecast(args: dict[str, Any]) -> dict[str, Any]:
    """
    Fetch weather forecast from yr.no API.

    Args:
        latitude: Latitude in decimal degrees (required)
        longitude: Longitude in decimal degrees (required)
        altitude: Elevation in meters (optional, for better accuracy)
        location_name: Human-readable location name (optional)
        units: 'fahrenheit' or 'celsius' (default: 'fahrenheit')

    Returns:
        Formatted weather forecast with current conditions and 3-day summary
    """
    # Extract and validate parameters
    latitude = args.get("latitude")
    longitude = args.get("longitude")
    altitude = args.get("altitude")
    location_name = args.get("location_name", "the location")
    units = args.get("units", "fahrenheit").lower()

    # Validate required parameters
    if latitude is None or longitude is None:
        return {
            "content": [{
                "type": "text",
                "text": "Error: Both latitude and longitude are required parameters."
            }],
            "is_error": True
        }

    # Validate coordinate ranges
    if not (-90 <= latitude <= 90):
        return {
            "content": [{
                "type": "text",
                "text": f"Error: Latitude must be between -90 and 90 degrees. Got: {latitude}"
            }],
            "is_error": True
        }

    if not (-180 <= longitude <= 180):
        return {
            "content": [{
                "type": "text",
                "text": f"Error: Longitude must be between -180 and 180 degrees. Got: {longitude}"
            }],
            "is_error": True
        }

    # Validate units
    if units not in ["fahrenheit", "celsius"]:
        units = "fahrenheit"

    # Build API URL
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact"
    params = {
        "lat": latitude,
        "lon": longitude
    }

    if altitude is not None:
        params["altitude"] = altitude

    # Required User-Agent header
    headers = {
        "User-Agent": "MarbellaAgent/1.0 (github.com/user/marbella-agent)"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as response:

                # Handle rate limiting
                if response.status == 429:
                    return {
                        "content": [{
                            "type": "text",
                            "text": "Weather API rate limit exceeded. Please try again in a few moments."
                        }],
                        "is_error": True
                    }

                # Handle other HTTP errors
                if response.status != 200:
                    return {
                        "content": [{
                            "type": "text",
                            "text": f"Weather API error: HTTP {response.status}. Unable to fetch forecast."
                        }],
                        "is_error": True
                    }

                data = await response.json()

    except aiohttp.ClientError as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Network error while fetching weather data: {str(e)}. Please check your connection and try again."
            }],
            "is_error": True
        }
    except Exception as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Unexpected error: {str(e)}"
            }],
            "is_error": True
        }

    # Parse weather data
    try:
        properties = data.get("properties", {})
        timeseries = properties.get("timeseries", [])

        if not timeseries:
            return {
                "content": [{
                    "type": "text",
                    "text": "No forecast data available for this location."
                }],
                "is_error": True
            }

        # Get current conditions (first entry)
        current = timeseries[0]
        current_data = current.get("data", {})
        instant = current_data.get("instant", {}).get("details", {})

        # Extract current weather
        current_temp = instant.get("air_temperature")
        wind_speed = instant.get("wind_speed", 0)
        wind_direction = instant.get("wind_from_direction", 0)
        humidity = instant.get("relative_humidity", 0)

        # Get next hours data for precipitation and symbol
        next_1h = current_data.get("next_1_hours", {})
        next_6h = current_data.get("next_6_hours", {})

        # Try to get weather symbol
        symbol_code = None
        if next_1h:
            symbol_code = next_1h.get("summary", {}).get("symbol_code")
        elif next_6h:
            symbol_code = next_6h.get("summary", {}).get("symbol_code")

        # Try to get precipitation
        precipitation = None
        if next_1h:
            precipitation = next_1h.get("details", {}).get("precipitation_amount")
        elif next_6h:
            precipitation = next_6h.get("details", {}).get("precipitation_amount")

        # Build forecast summary for next 3 days
        forecast_days = []

        # Group by day (take samples every 6 hours for 3 days)
        for i in range(0, min(len(timeseries), 72), 6):  # 3 days * 24 hours / 6-hour intervals
            entry = timeseries[i]
            entry_data = entry.get("data", {})
            entry_instant = entry_data.get("instant", {}).get("details", {})

            day_temp = entry_instant.get("air_temperature")

            # Get symbol for this period
            day_next_6h = entry_data.get("next_6_hours", {})
            day_symbol = day_next_6h.get("summary", {}).get("symbol_code", "unknown")

            if day_temp is not None:
                forecast_days.append({
                    "time": entry.get("time", ""),
                    "temp": day_temp,
                    "symbol": day_symbol
                })

        # Format the response
        response_text = f"**Weather Forecast for {location_name}**\n\n"

        # Current conditions
        response_text += "**Current Conditions:**\n"
        if current_temp is not None:
            response_text += f"- Temperature: {format_temperature(current_temp, units)}\n"
        response_text += f"- Wind: {wind_speed:.1f} m/s from {wind_direction:.0f}°\n"
        response_text += f"- Humidity: {humidity:.0f}%\n"

        if precipitation is not None and precipitation > 0:
            response_text += f"- Precipitation: {precipitation:.1f} mm\n"

        if symbol_code:
            # Convert symbol code to readable description
            weather_desc = symbol_code.replace("_", " ").title()
            response_text += f"- Conditions: {weather_desc}\n"

        # 3-day forecast summary
        response_text += "\n**3-Day Forecast:**\n"

        days_shown = 0
        for i, day in enumerate(forecast_days):
            if days_shown >= 3:
                break

            # Only show one entry per day (skip similar times)
            if i % 4 == 0:  # Roughly one per day
                time_str = day["time"][:10]  # Extract date
                temp_str = format_temperature(day["temp"], units)
                conditions = day["symbol"].replace("_", " ").title()

                response_text += f"\n- {time_str}: {temp_str}, {conditions}"
                days_shown += 1

        response_text += "\n\n---\n"
        response_text += f"Coordinates: {latitude}°, {longitude}°"
        if altitude:
            response_text += f" at {altitude}m elevation"
        response_text += "\nData provided by yr.no / Norwegian Meteorological Institute"

        return {
            "content": [{
                "type": "text",
                "text": response_text
            }]
        }

    except (KeyError, ValueError, TypeError) as e:
        return {
            "content": [{
                "type": "text",
                "text": f"Error parsing weather data: {str(e)}. The API response format may have changed."
            }],
            "is_error": True
        }
