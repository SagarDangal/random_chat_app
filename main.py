from fastapi import status,File, UploadFile,Depends,HTTPException,APIRouter,Header, Request
from bson.objectid import ObjectId
from typing import List, Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.responses import HTMLResponse
import uvicorn
from app import create_app
from app.chats import send_message_to_channel
import random
from fastapi.templating import Jinja2Templates
import json

app = create_app()

templates = Jinja2Templates(directory="templates")
router = APIRouter(
)

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("random_chat.html", {"request": request})

@app.get("/items/chat/", response_class=HTMLResponse)
async def read_item(request: Request, username: Optional[str] = 'test'):
    return templates.TemplateResponse("new_chat.html", {"request": request, "id": username})


@app.post("/items/chat/",status_code=204)
async def read_items(request: Request):
    return {'id': True}

class ConnectionManager:

    def __init__(self):
        self.random_client_pair = {}
        self.active_available : List[WebSocket]=[]
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket,client_id:str):
        [self.active_connections.remove(item) for item in self.active_connections if item[1] == client_id]
        await websocket.accept()
        self.active_connections.append((websocket,client_id))
        self.active_available.append((websocket,client_id))

    def disconnect(self, websocket: WebSocket,client_id:str):

        self.active_connections.remove((websocket,client_id))
        try:
            self.active_available.remove((websocket,client_id))
        except:
            pass    

    async def send_personal_message(self, message: str, websocket: WebSocket):

        await websocket.send_text(message)

    async def broadcast(self, message: str,client):
        try:
            await self.random_client_pair[str(client)][0].send_text(message)
        except:
            pass    
        # for connection in self.active_connections:
        #     if connection[1] in channel:
        #         await connection[0].send_json(message)
    def choose_random(self,websocket,user):
        random_true = True
        while random_true:
            try:
                 return  self.random_client_pair[str(user)]
            except :
                
                #try:
                    #self.active_available.remove(str(user))
                    user_2 =    random.choice(self.active_available)
                    print(user_2[1],user)
                    print(self.active_available)
                    print('pair', self.random_client_pair)
                    if (user_2[1] != str(user)) and str(user) != '' and user_2[1] != '':
        #             user_obj = i 
        #             self.active_available.remove(i)
                        self.random_client_pair[user_2[1]] = (websocket, str(user))
                        self.random_client_pair[str(user)] = user_2
                        print(self.random_client_pair)
                        self.active_available.remove(user_2)
                        self.active_available.remove((websocket,str(user)))
                        return self.random_client_pair[str(user)]
                    random_true = False    
                #except:
                #    random_true = False



        #     user_obj =''
        #     for i in self.active_connections:
        #         print(i,user)

        #       
        #     #try:         
        #     user_1 = random.choice(self.active_available)
        #     #self.active_available.remove(user_1)
        #             # user_2 =    random.choice(self.active_available)
        #             # active_available.remove(user_2) 

        #     self.random_client_pair[user_1[1]] = user_obj
        #     self.random_client_pair[user] = user_1
           
        #     print(self.random_client_pair)
        #     #except:
            #        pass

            #return self.random_client_pair[user]    
    def delete_pair(self,user):
        del self.random_client_pair[user]    
               

manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(client_id:str, websocket: WebSocket):

    # 1、 client 、 The server establishes  ws  Connect 

    await manager.connect(websocket,client_id)
    random_client_pair = manager.choose_random(websocket,client_id)
    print('random', random_client_pair)
    if random_client_pair:
        await manager.send_personal_message(f'user_connected', websocket)
        await manager.send_personal_message(f'user_connected', random_client_pair[0])

    # 2、 Broadcast a client into the chat room 

    #await manager.broadcast(f"{client_id}  Into the chat room ")

    try:

        while True:

            # 3、 The server receives the content sent by the client 

            data = await websocket.receive_json()
            print(type(data))
            print(data)
            datas = json.dumps(data)

            # 4、 Broadcast a message sent by a client 
            #client = send_message_to_channel(data['sendFrom'],data['message'],data['channel_id'],'text')
            
            #client = manager.choose_random(data['sendFrom'])
            #print(client)
            #if random_client_pair:
            await manager.broadcast(f"{datas}",client_id)

            # 5、 The server replies to the client 

            await manager.send_personal_message(f"{datas}", websocket)
    except WebSocketDisconnect:

    #     # 6、 If a client is disconnected , Broadcast a client left 

         manager.disconnect(websocket,client_id)
         #manager.delete_pair(client_id)
        

        #await manager.broadcast(f"{client_id}  Left the chat room ")


if __name__ == "__main__":
    uvicorn.run("main:app")
    