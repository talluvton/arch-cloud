import logging
from pymongo import MongoClient, ASCENDING, ReturnDocument
from pymongo.collection import Collection
from settings import MONGO_URI, DB_NAME, COLLECTION_NAME
from models.architecture import Architecture

logger = logging.getLogger(__name__)

_client = MongoClient(MONGO_URI)
_db = _client[DB_NAME]
collection: Collection = _db[COLLECTION_NAME]

try:
    collection.create_index([("source", ASCENDING)], unique=True)
    logger.info("Ensured unique index on 'source'")
except Exception as e:
    logger.warning("Could not create index on 'source': %s", e)

def get_collection() -> Collection:
    return collection

def upsert_architecture(arch: Architecture) -> dict:
    doc = arch.model_dump(by_alias=True, exclude={"_id"}, exclude_none=True, mode="json")
    set_fields = {k: v for k, v in doc.items() if k != "timestamp"}
    set_on_insert = {"timestamp": doc.get("timestamp")}
    updated = collection.find_one_and_update(
        {"source": doc["source"]},
        {"$set": set_fields, "$setOnInsert": set_on_insert},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return updated