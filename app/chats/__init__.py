from fastapi import status,File, UploadFile,Depends,HTTPException,APIRouter,Header
from bson.objectid import ObjectId
from typing import List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.responses import HTMLResponse
from app.db.deps import db
from .utils.decorators import userValidate
from . import crud
from . import schemas
from . import models
import datetime





router = APIRouter(
    prefix = "/chats"
)


@router.get("/channel")
async def get_channels(user:str,User: Optional[str] = Header(None)):
    items =list(db['Channels'].find().sort('last_modified', -1))
    data =[]
    for item in items:
        if user in item['Users']:
            channel = {
                "channel_id": str(item['_id']),
                "users":item['Users'],
            }
            try:
                channel["last_message"]=item['Message'][-1]
                channel["status"]=item['status']
            except:
                pass
            data.append(channel)
    
    return data


@router.post("/channel/")
async def create_channel(admin:str,users:schemas.UserList,User: Optional[str] = Header(None)):
    try:
        old_channels = db["Channels"].find_one({"Users": users.users })
        print(old_channels['_id'])
        if old_channels['_id']:
            return {"id":str(old_channels['_id'])}
    except:        
        channels = db["Channels"].insert_one({'admin':admin,"Users":users.users,'convertation_start': False})    
        return {"id":str(channels.inserted_id)}


@router.post("/channel/add_user")
async def add_user_to_room(user:str,channel_id:str,User: Optional[str] = Header(None)):
    db["Channels"].find_one_and_update({"_id": ObjectId(channel_id)},{'$push': {'Users':user}})


#@router.post("/channel/send_message")
#@userValidate
def send_message_to_channel(user:str,message:str,channel_id:str,message_type:str = None):
    channel = db["Channels"].find_one({"_id": ObjectId(channel_id)})
    try:
        if channel['block']:
            return []
    except:
        pass        
    db["Channels"].find_one_and_update({"_id": ObjectId(channel_id)},{'$push': {'Message':{"sentBy":user,"message": message,"date": datetime.datetime.utcnow(),"message_type":message_type}}})
    db["Channels"].find_one_and_update({"_id": ObjectId(channel_id)},{'$set': {'status':schemas.Status.UNSEEN,"last_modified": datetime.datetime.utcnow()}})
    
    try:
        if (user != channel['admin']):
            db["Channels"].find_one_and_update({"_id": ObjectId(channel_id)},{'$set': {'convertation_start': True}})
    except:
        pass            
    return channel['Users']

@router.post("/channel/update_message_status")
def update_message_status(channel_id:str,User: Optional[str] = Header(None)):
    db["Channels"].find_one_and_update({"_id": ObjectId(channel_id)},{'$set': {'status':schemas.Status.SEEN}})
    user = db["Channels"].find_one({"_id": ObjectId(channel_id)})
    return {"status":schemas.Status.SEEN}    


@router.get("/channel/get_message")
def get_message_of_channel(user:str,channel_id:str,User: Optional[str] = Header(None)):
    message = db["Channels"].find_one({"_id": ObjectId(channel_id)})
    try:
        if message['block']:
            return []
    except:
        pass 
    try:
    	return message['Message'][::-1]
    except:
    	return []


@router.post("/channel/block")
def block_channel(user:str,channel_id:str,User: Optional[str] = Header(None)):
    db["Channels"].find_one_and_update({"_id": ObjectId(channel_id)},{'$set': {'block':True}})
    return {"channel_Id":channel_id,'block':True}


@router.post("/channel/unblock")
def unblock_channel(user:str,channel_id:str,User: Optional[str] = Header(None)):
    db["Channels"].find_one_and_update({"_id": ObjectId(channel_id)},{'$set': {'block':False}})
    return {"channel_Id":channel_id,'block':True}


@router.post("/channel/accept")
def accept_channel(user:str,channel_id:str,User: Optional[str] = Header(None)):
    db["Channels"].find_one_and_update({"_id": ObjectId(channel_id)},{'$set': {'convertation_start': True}})
    return {"channel_Id":channel_id,'convertation_start': True}


@router.delete("/channel/")
def delete_channel(user:str,channel_id:str,User: Optional[str] = Header(None)):
    channel = db["Channels"].find_one({"_id": ObjectId(channel_id)})
    channel.drop()
    return {"channel_Id":channel_id,'delete':True}          






html = """

<!DOCTYPE html>

<html>

    <head>

        <title>Chat</title>

    </head>

    <body>

        <h1>WebSocket Chat</h1>

        <h2>Your ID: <span id="ws-id"></span></h2>

        <form action="" onsubmit="sendMessage(event)">

            <input type="text" id="messageText" placeholder="Your message" autocomplete="off"/>
            
            <input type="text" id="channel_id" placeholder="channel_Id" autocomplete="off"/>

            <button>Send</button>

        </form>

        <ul id='messages'>

        </ul>

        <script>

            var client_id = Date.now()

            document.querySelector("#ws-id").textContent = client_id;

            var ws = new WebSocket(`ws://127.0.0.1:8000/ws/${client_id}`);

            ws.onmessage = function(event) {

                var messages = document.getElementById('messages')

                var message = document.createElement('li')

                var content = document.createTextNode(event.data)

                message.appendChild(content)

                messages.appendChild(message)

            };

            function sendMessage(event) {

                var input = document.getElementById("messageText")
                var channel = document.getElementById("channel_id")
                var data = {
                    "sendFrom":client_id,
                    "channel_id":channel.value,
                    "message":input.value
                }

                ws.send(JSON.stringify(data))

                input.value = ''

                event.preventDefault()

            }

        </script>

    </body>

</html>

"""



#  Return to a paragraph  HTML  Code to the front end 

@router.get("/")

async def get():

    return HTMLResponse(html)

#  Process and broadcast messages to multiple  WebSocket  Connect 
