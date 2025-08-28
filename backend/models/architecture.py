from datetime import datetime, timezone
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, HttpUrl, field_serializer, ConfigDict, field_validator
from bson import ObjectId

Role = Literal[
    "Compute","Storage","Database","Networking","Security",
    "Monitoring","Integration","Analytics","DevOps","Other"
]


class ScrapeReq(BaseModel):
    url: str

class Service(BaseModel):
    name: str
    role: Role = "Other"

class Architecture(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    source: HttpUrl
    provider: Optional[str] = None
    services: List[Service]
    flow: List[str] = []
    features: List[str] = []

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("id", mode="before")
    @classmethod
    def _objectid_to_str(cls, v):
        return str(v) if isinstance(v, ObjectId) else v

    @field_serializer("timestamp")
    def _serialize_timestamp(self, dt: datetime) -> str:
        if dt.tzinfo:
            dt = dt.astimezone(timezone.utc)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
