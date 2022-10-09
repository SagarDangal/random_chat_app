
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from enum import Enum

class Status(str,Enum):
    SEEN = 'SEEN'
    UNSEEN = 'UNSEEN'
    
class Message_Type(str,Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'   

class MessageStatus(BaseModel):
    status : Status 
    

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')

        return str(v)
class Users(BaseModel):

    userId: str =Field(...)

class UserList(BaseModel):

    users : List[str]

    class Config:
        orm_mode= True
        arbitrary_types_allowed = True
        

class Channel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    admin: str = Field(...)
    
    users: List[str]

    message: str = Field(...)

    channel_name: str


    


    

