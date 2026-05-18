from fastapi import FastAPI, WebSocket
import asyncio

from app.websocket_manager import manager
from app.listener import listen_for_changes

app = FastAPI()


@app.on_event("startup")
async def startup_event():

    asyncio.create_task(listen_for_changes())


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except:
        manager.disconnect(websocket)