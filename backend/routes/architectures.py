from typing import List
from fastapi import APIRouter
from db import get_collection
from models.architecture import Architecture

router = APIRouter(prefix="/architectures", tags=["Architectures"])
_coll = get_collection()


@router.get("/", response_model=List[Architecture], response_model_by_alias=False)
def get_architectures():
    docs = _coll.find().sort("timestamp", -1)
    return [Architecture.model_validate(d) for d in docs]


