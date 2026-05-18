import psycopg
from app.config import DATABASE_URL


def listen_for_changes():
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        
        with conn.cursor() as cur:
            cur.execute("LISTEN order_changes;")

            print("Listening for PostgreSQL notifications...")

            for notify in conn.notifies():
                print(f"Received notification: {notify.payload}")


listen_for_changes()