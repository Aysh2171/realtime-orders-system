from fastapi import FastAPI, WebSocket, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import asyncio

from app.websocket_manager import manager
from app.listener import listen_for_changes

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def startup_event():

    asyncio.create_task(listen_for_changes())


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await asyncio.sleep(1)

    except:
        manager.disconnect(websocket)