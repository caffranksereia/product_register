import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import errors

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
                port=int(os.getenv("DB_PORT", "5432")),
            )

            print("✅ Connected to database...")
            return con

        except errors.InvalidCatalogName:
            if attempt == 0:
                print("⚠️ Database does not exist.")
                create_database()
            else:
                print("❌ Database could not be created.")

        except psycopg2.Error as error:
            print(f"❌ Attempt {attempt + 1} failed: {error}")

            if attempt == max_retries - 1:
                print("❌ Could not connect to database.")

    return None
