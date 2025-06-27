from bson import ObjectId as _ObjectId
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, BeforeValidator #, ConfigDict
from typing import Annotated, Optional
from datetime import datetime


def check_object_id(value: str) -> str:
    if not _ObjectId.is_valid(value):
        raise ValueError('Invalid ObjectId')
    return value

PyObjectId = Annotated[str, BeforeValidator(check_object_id)]


class MongoMethods:
    '''usage
    d = model.from_mongo(d)
    d = model(**d).to_mongo()
    '''
    @classmethod
    def from_mongo(cls, d: dict):
        d['_id'] = str(d['_id'])
        return cls(**d)

    def to_mongo(self) -> dict:
        d = self.model_dump()
        if 'id' in d.keys():
            d["_id"] = ObjectId(d.pop('id'))
        return d


class Species(BaseModel, MongoMethods):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    field: int
    family: str
    species: str
    sort_no: int
    # model_config = ConfigDict(arbitrary_types_allowed=True)


class Variety(BaseModel, MongoMethods):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    parent: Optional[PyObjectId]
    variety: str
    sort_no: int


class Growth(BaseModel, MongoMethods):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    parent: Optional[PyObjectId]
    title: str


class Records(BaseModel, MongoMethods):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    parent: Optional[PyObjectId]
    date: datetime
    title: str
    description: str
    image: str


class Document(BaseModel, MongoMethods):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    parent: Optional[PyObjectId]
    species: str
    variety: str
    document: str