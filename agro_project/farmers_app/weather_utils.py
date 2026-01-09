import requests
from django.conf import settings
from datetime import datetime
from .db_connection import get_locations_collection


def store_weather_report(lat, lon):
    locations_collection = get_locations_collection()
    weather_data = None
    weather_stored = False


    try:
        onecall_params = {
            "lat": lat,
            "lon": lon,
            "exclude": "minutely,hourly,alerts",
            "appid": settings.OPENWEATHER_API_KEY,
            "units": "metric"
        }
        onecall_response = requests.get(
            settings.OPENWEATHER_ONECALL_URL,
            params=onecall_params,
            timeout=10
        )
        onecall_response.raise_for_status()

        onecall_json = onecall_response.json()
        current = onecall_json.get("current", {})
        weather = current.get("weather", [{}])[0]

        weather_data = {
            'temperature': round(current.get("temp", 0), 1),
            'feels_like': round(current.get("feels_like", 0), 1),
            'humidity': current.get("humidity", 0),
            'pressure': current.get("pressure", 0),
            'weather_description': weather.get("description", ""),
            'icon': weather.get("icon", ""),
            'wind_speed': round(current.get("wind_speed", 0), 1),
            'clouds': current.get("clouds", 0),
            'uvi': current.get("uvi", 0),
            'visibility': current.get("visibility", 0),
            'dew_point': round(current.get("dew_point", 0), 1) if current.get("dew_point") else None
        }
        weather_stored = True

    except requests.RequestException:

        try:
            weather_url = f"{settings.OPENWEATHER_API_URL}?lat={lat}&lon={lon}&appid={settings.OPENWEATHER_API_KEY}&units=metric"
            weather_response = requests.get(weather_url, timeout=10)
            weather_response.raise_for_status()

            weather_json = weather_response.json()
            weather_info = weather_json.get('weather', [{}])[0]

            weather_data = {
                'location': weather_json.get('name', 'Unknown'),
                'temperature': round(weather_json['main']['temp'], 1),
                'feels_like': round(weather_json['main']['feels_like'], 1),
                'description': weather_info.get('description', '').title(),
                'humidity': weather_json['main']['humidity'],
                'pressure': weather_json['main']['pressure'],
                'wind_speed': round(weather_json.get('wind', {}).get('speed', 0), 1),
                'clouds': weather_json.get('clouds', {}).get('all', 0),
                'icon': weather_info.get('icon', ''),
                'weather_description': weather_info.get('description', '')
            }
            weather_stored = True

        except requests.RequestException as e:
            return {
                "status": "error",
                "message": str(e)
            }


    location_doc = {
        'latitude': lat,
        'longitude': lon,
        'timestamp': datetime.now(),
        'source': 'weather_utils'
    }


    if weather_data:
        location_doc['weather'] = weather_data
        location_doc['weather_fetched'] = True
    else:
        location_doc['weather_fetched'] = False


    result = locations_collection.insert_one(location_doc)
    stored_id = str(result.inserted_id)

    if weather_stored:
        return {
            "status": "success",
            "message": f"Weather report saved for ({lat}, {lon})",
            "report_id": stored_id,
            "weather": weather_data
        }
    else:
        return {
            "status": "success",
            "message": f"Location saved for ({lat}, {lon}), but weather data could not be fetched",
            "report_id": stored_id
        }