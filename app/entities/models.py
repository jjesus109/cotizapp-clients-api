from enum import Enum
from typing import TypedDict, Optional

from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class Client(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    location: str = Field(...)
    email: str = Field(...)
    phone_number: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ClientUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]
    email: Optional[str]
    phone_number: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ClientDict(TypedDict):
    id: str
    name: str
    location: str
    email: str
    phone_number: int


class MessageType(Enum):
    client = "Client"


class MessageFormat(BaseModel):
    type: str
    content: Client
