import os

import psycopg2
from dotenv import load_dotenv
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

load_dotenv(".env")


def create_database() -> bool:
    db_name = os.getenv("DB_NAME")

    if not db_name:
        raise ValueError("DB_NAME not configured in .env")

    con = None

    try:
        con = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname="postgres",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=int(os.getenv("DB_PORT", "5432")),
        )

        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with con.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM pg_database
                WHERE datname = %s;
                """,
                (db_name,),
            )

            if cursor.fetchone():
                print(f"⏭️ Database '{db_name}' already exists. Skipping.")
                return True

            cursor.execute(
                sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
            )

            print(f"✅ Database '{db_name}' created!")

        return True

    except psycopg2.Error as error:
        print(f"❌ Error creating database: {error}")
        raise

    finally:
        if con is not None:
            con.close()
