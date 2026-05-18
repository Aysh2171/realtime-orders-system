import psycopg
import asyncio

from app.config import DATABASE_URL
from app.websocket_manager import manager


async def listen_for_changes():

    conn = psycopg.connect(DATABASE_URL, autocommit=True)

    conn.execute("LISTEN order_changes;")

    print("Listening for PostgreSQL notifications...")

    while True:

        notifications = conn.notifies(timeout=1)

        for notify in notifications:

            print(f"Received notification: {notify.payload}")

            await manager.broadcast(notify.payload)

        await asyncio.sleep(0.1)