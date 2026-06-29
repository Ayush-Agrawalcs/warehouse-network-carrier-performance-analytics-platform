import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
import socket

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

host = os.getenv("DB_HOST")
print("HOST =", repr(os.getenv("DB_HOST")))
print("DNS =", socket.gethostbyname(host))

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )