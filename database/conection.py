import os

import psycopg2
from dotenv import load_dotenv

from .db_setup import create_database

load_dotenv(".env")


def get_connection():
    max_retries = 3

    for attempt in range(max_retries):
        try:
            con = psycopg2.connect(
                host=os.getenv("DB_HOST"),
                database=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                port=5432,
            )
            print("✅ Connected to database...")
            return con

        except Exception as e:
            print(f"❌ Attempt {attempt + 1} failed:{e}")
            if attempt == 0:
                print("⚠️ Trying to create database...")
                create_database()
            else:
                print("❌ Could not connect.")

    return None
