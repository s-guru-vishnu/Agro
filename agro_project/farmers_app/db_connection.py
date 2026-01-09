from functools import lru_cache
from typing import Any, Iterable, List

from django.conf import settings
from pymongo import MongoClient


@lru_cache(maxsize=1)
def get_mongo_client() -> MongoClient:
    mongo_settings = getattr(settings, "MONGODB_SETTINGS", {}) or {}
    host = mongo_settings.get("host") or "mongodb://localhost:27017/"
    client_kwargs: dict[str, Any] = {"host": host}
    username = mongo_settings.get("username")
    password = mongo_settings.get("password")
    if username and password:
        client_kwargs["username"] = username
        client_kwargs["password"] = password
    return MongoClient(**client_kwargs)


def get_database():
    mongo_settings = getattr(settings, "MONGODB_SETTINGS", {}) or {}
    db_name = mongo_settings.get("db") or "agro-db"
    return get_mongo_client()[db_name]


def get_services_collection():
    return get_database()["services"]


def _get_collection_by_candidates(candidates: Iterable[str]):
    candidates = list(candidates)
    if not candidates:
        raise ValueError("At least one collection name must be provided")

    db = get_database()
    existing_collections: List[str] = db.list_collection_names()
    for name in candidates:
        if name in existing_collections:
            return db[name]

    return db[candidates[0]]


def get_fertilizers_collection():
    return _get_collection_by_candidates(["fertilizers", "Fertilizers"])


def get_machines_collection():
    return _get_collection_by_candidates(["machines", "Machine", "Machines"])


def get_manpower_collection():
    return _get_collection_by_candidates(["manpower", "Manpower"])