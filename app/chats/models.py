from enum import Enum

class Status(Enum):
    SEEN = 'SEEN'
    UNSEEN = 'UNSEEN'
    
class Message_Type(Enum):
    TEXT = 'TEXT'
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'    


