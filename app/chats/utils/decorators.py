
from app.db.deps import db
from functools import wraps


def adminValidate(func):
    @wraps(func)
    def inner(*args, **kwargs):
         if  kwargs['User'] != db["Channels"].find_one({"channel_name": channel_name})['admin']:
            raise HTTPException(status_code=403,detail="forbidden")   
         return func(*args, **kwargs)
    return inner

def userValidate(func):
    @wraps(func)
    def inner(*args, **kwargs):
         if  kwargs['User'] in db["Channels"].find_one({"_id": kwargs('channel_id')})['users']:
            raise HTTPException(status_code=403,detail="forbidden")   
         return func(*args, **kwargs)
    return inner




   

