import time
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")

def wait_for_db():
    while True:
        try:
            engine = create_engine(DATABASE_URL)
            conn = engine.connect()
            conn.close()
            print("Database connected")
            break
        except Exception:
            print("Waiting for database...")
            time.sleep(2)