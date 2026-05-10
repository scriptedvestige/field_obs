import os
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    # Using test db creds on laptop, real db creds on Pi
    return connect(
        host=os.getenv("TEST_DB_HOST"),
        dbname=os.getenv("TEST_DB_NAME"),
        user=os.getenv("TEST_DB_USER"),
        password=os.getenv("TEST_DB_PASS"),
        port=int(os.getenv("TEST_DB_PORT")),
        cursor_factory=RealDictCursor
    )