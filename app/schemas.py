from pydantic import BaseModel, Field
from bson.objectid import ObjectId


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class TodoSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    author: str
    title: str
    description: str
    is_completed: bool

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "author": "Guido van Rossum",
                "title": "lets talk about python",
                "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ips",
                "is_completed": True
            }
        }


class TodoUpdateSchema(BaseModel):
    author: str
    title: str
    description: str
    is_completed: bool

    class Config:
        schema_extra = {
            "example": {
                "author": "Guido van Rossum",
                "title": "lets talk about python",
                "description": "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ips",
                "is_completed": True
            }
        }
