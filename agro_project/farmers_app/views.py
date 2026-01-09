from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from datetime import datetime
import json
import math
import re
import requests

from .db_connection import (
    get_fertilizers_collection,
    get_machines_collection,
    get_manpower_collection,
)

def index(request):
    return render(request, 'farmers_app/index.html')

def fertilizers_page(request):
    return render(request, 'farmers_app/fertilizers.html')

def machines_page(request):
    return render(request, 'farmers_app/machines.html')

def manpower_page(request):
    return render(request, 'farmers_app/man-power.html')

def sellers_page(request):
    return render(request, 'farmers_app/sellers.html')


def _safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _calculate_distance_km(lat1, lon1, lat2, lon2):
    radius_earth_km = 6371
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return radius_earth_km * c


def _serialize_service(doc, user_lat=None, user_lon=None, radius_km=None, service_type=None):
    if not doc:
        return None

    location = doc.get('location') or {}
    doc_lat = _safe_float(location.get('latitude'))
    doc_lon = _safe_float(location.get('longitude'))
    distance_km = None

    if user_lat is not None and user_lon is not None and doc_lat is not None and doc_lon is not None:
        distance_km = _calculate_distance_km(user_lat, user_lon, doc_lat, doc_lon)
        if radius_km is not None and distance_km > radius_km:
            return None

    serialized = {
        '_id': str(doc.get('_id')),
        'name': doc.get('name'),
        'description': doc.get('description'),
        'service_type': doc.get('service_type') or service_type,
        'availability': doc.get('availability', True),
        'location': {
            'address': location.get('address'),
            'city': location.get('city'),
            'state': location.get('state'),
            'pincode': location.get('pincode'),
            'latitude': doc_lat,
            'longitude': doc_lon,
        },
        'price': doc.get('price'),
        'price_unit': doc.get('price_unit'),
        'quantity': doc.get('quantity'),
        'unit': doc.get('unit'),
        'type': doc.get('type'),
        'skills': doc.get('skills'),
        'experience': doc.get('experience'),
        'rate': doc.get('rate'),
    }
    created_at = doc.get('created_at')
    if isinstance(created_at, datetime):
        serialized['created_at'] = created_at.isoformat()

    if distance_km is not None:
        serialized['distance_km'] = round(distance_km, 1)


    return {k: v for k, v in serialized.items() if v is not None and v != {}}


SERVICE_COLLECTION_MAP = {
    'fertilizer': get_fertilizers_collection,
    'machine': get_machines_collection,
    'manpower': get_manpower_collection,
}


def _get_services(service_type, limit, city=None, user_lat=None, user_lon=None, radius_km=None):
    collection_factory = SERVICE_COLLECTION_MAP.get(service_type)
    if not collection_factory:
        return []

    collection = collection_factory()
    query = {}
    if city:
        regex = re.compile(re.escape(city), re.IGNORECASE)
        query['location.city'] = regex


    fetch_limit = min(limit * 3, 300)
    cursor = collection.find(query).sort('created_at', -1).limit(fetch_limit)
    results = []
    for doc in cursor:
        serialized = _serialize_service(
            doc,
            user_lat=user_lat,
            user_lon=user_lon,
            radius_km=radius_km,
            service_type=service_type,
        )
        if serialized:
            results.append(serialized)
        if len(results) >= limit:
            break
    return results


@require_http_methods(["GET"])
def get_availability(request):
    service_type = request.GET.get('type')
    city = request.GET.get('city', '').strip() or None

    user_lat = _safe_float(request.GET.get('latitude'))
    user_lon = _safe_float(request.GET.get('longitude'))
    radius_km = _safe_float(request.GET.get('radius'))

    try:
        limit = int(request.GET.get('limit', 50))
    except (TypeError, ValueError):
        limit = 50
    limit = max(1, min(limit, 100))

    type_map = {
        'fertilizer': 'fertilizers',
        'machine': 'machines',
        'manpower': 'manpower',
    }

    if service_type and service_type not in type_map:
        return JsonResponse({
            'success': False,
            'error': "Invalid 'type' parameter. Use fertilizer, machine, or manpower."
        }, status=400)

    response_data = {'success': True}

    try:
        if service_type:
            key = type_map[service_type]
            response_data[key] = _get_services(
                service_type,
                limit,
                city=city,
                user_lat=user_lat,
                user_lon=user_lon,
                radius_km=radius_km if (user_lat is not None and user_lon is not None) else None,
            )
        else:
            for stype, key in type_map.items():
                response_data[key] = _get_services(
                    stype,
                    limit,
                    city=city,
                    user_lat=user_lat,
                    user_lon=user_lon,
                    radius_km=radius_km if (user_lat is not None and user_lon is not None) else None,
                )

        return JsonResponse(response_data)
    except Exception as exc:
        print(f"Error fetching availability: {exc}")
        return JsonResponse({
            'success': False,
            'error': 'Unable to load availability data. Please try again later.'
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def chatbot_api(request):

    RAG_WEBHOOK_URL = getattr(settings, 'RAG_MODEL_WEBHOOK_URL', None)


    if not RAG_WEBHOOK_URL:
        return JsonResponse({
            'success': False,
            'error': 'RAG webhook URL is not configured. Please set RAG_MODEL_WEBHOOK_URL in your .env file.'
        }, status=500)

    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()

        if not message:
            return JsonResponse({
                'success': False,
                'error': 'Message cannot be empty'
            }, status=400)


        user_latitude = data.get('latitude')
        user_longitude = data.get('longitude')


        webhook_payload = {
            'message': message,
        }


        if user_latitude and user_longitude:
            webhook_payload['latitude'] = user_latitude
            webhook_payload['longitude'] = user_longitude


        try:
            response = requests.post(
                RAG_WEBHOOK_URL,
                json=webhook_payload,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            response.raise_for_status()


            webhook_response = response.json()


            if isinstance(webhook_response, dict):

                response_text = (
                    webhook_response.get('response') or
                    webhook_response.get('message') or
                    webhook_response.get('answer') or
                    webhook_response.get('text') or
                    webhook_response.get('data')
                )


                if response_text is None:
                    response_text = json.dumps(webhook_response)
                elif isinstance(response_text, dict):
                    response_text = json.dumps(response_text)
            elif isinstance(webhook_response, str):
                response_text = webhook_response
            else:

                response_text = str(webhook_response)

            if not response_text:
                response_text = "I received your message but couldn't generate a response. Please try again."

            return JsonResponse({
                'success': True,
                'response': response_text
            })

        except requests.exceptions.Timeout:
            return JsonResponse({
                'success': False,
                'error': 'The request to the AI service timed out. Please try again.'
            }, status=504)

        except requests.exceptions.RequestException as e:

            print(f"Error calling RAG webhook: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Unable to connect to AI service. Please try again later.'
            }, status=502)

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON format'
        }, status=400)
    except Exception as e:

        print(f"Unexpected error in chatbot_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'An unexpected error occurred. Please try again.'
        }, status=500)

def generate_chatbot_response(message):
    message_lower = message.lower()


    if any(word in message_lower for word in ['fertilizer', 'fertilizers', 'nutrients', 'npk']):
        return "I can help you with fertilizers! You can check the Fertilizer Availability section on the left, or visit the Fertilizers page to see all available options. Would you like to know about specific types of fertilizers or their availability?"

    elif any(word in message_lower for word in ['machine', 'machines', 'tractor', 'harvester', 'equipment']):
        return "I can assist you with farming machinery! Check the Machine Availability section on the left, or visit the Machines page for rental options. Are you looking for tractors, harvesters, or other equipment?"

    elif any(word in message_lower for word in ['manpower', 'labor', 'workers', 'workers', 'staff', 'help']):
        return "I can help you find manpower! Check the Manpower Availability section on the left, or visit the Manpower page to connect with workers. What type of labor services do you need?"

    elif any(word in message_lower for word in ['crop', 'crops', 'planting', 'harvest', 'cultivation']):
        return "I can provide advice on crop management! I can help with planting schedules, harvesting times, and crop care. What specific information do you need about crops?"

    elif any(word in message_lower for word in ['weather', 'rain', 'temperature', 'climate']):
        return "I can help you with weather information! Click the 'Get My Location & Weather' button in the chatbot header to get current weather data for your location. This will help you plan your farming activities."

    elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm your AI Farming Assistant. I'm here to help you with fertilizers, machines, manpower, and crop management. How can I assist you today?"

    elif any(word in message_lower for word in ['thank', 'thanks']):
        return "You're welcome! Feel free to ask me anything else about farming. I'm here to help!"

    else:
        return "I understand you're asking about: \"" + message + "\". I'm here to help with fertilizers, machines, manpower, and crop management. Could you provide more details, or would you like me to guide you to specific sections?"