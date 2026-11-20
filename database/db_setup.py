import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2 import errors

load_dotenv(".env")


def create_database():
    con = None
    cursor = None
    try:
        con = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            dbname="postgres",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=5432,
        )
        con.autocommit = True
        cursor = con.cursor()
        db_name = os.getenv("DB_NAME")

        print("🔧 Setting up database...")
        cursor.execute(f"CREATE DATABASE {db_name}  ")
        print("✅ Database created!")

    except errors.DuplicateDatabase:
        print("⚠️ Database already exists.")
    except Exception as e:
        print(f"❌  Error creating database: {e} ")
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()


def ensure_schema_migrations_table(con):
    cursor = con.cursor()

    try:
        cursor.execute("""
            CREATE EXTENSION IF NOT EXISTS pgcrypto;
            """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                file_name VARCHAR(255) NOT NULL UNIQUE,
                executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """)
        con.commit()
        print("✅ schema_migrations table ready.")

    except Exception as e:
        con.rollback()
        print(f"❌ Error ensuring schema_migrations table: {e}")
        raise

    finally:
        cursor.close()


def get_applied_migrations(con):
    cur = con.cursor()

    try:
        cur.execute("""
            SELECT file_name
            FROM schema_migrations
            """)

        rows = cur.fetchall()
        return {row[0] for row in rows}

    finally:
        cur.close()


def mark_migration_as_applied(con, file_name):
    cursor = con.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO schema_migrations (file_name)
            VALUES (%s)
            ON CONFLICT (file_name) DO NOTHING
            """,
            (file_name,),
        )
        con.commit()

    except Exception as e:
        con.rollback()
        print(f"❌ Error marking migration as applied: {e}")
        raise

    finally:
        cursor.close()


def run_migrations(con):
    migrations_path = Path(__file__).parent / "migrations"
    migration_files = sorted(migrations_path.glob("*.sql"))

    ensure_schema_migrations_table(con)
    applied = get_applied_migrations(con)

    for file in migration_files:
        if file.name == "000_create_schema_migrations.sql":
            continue

        if file.name in applied:
            print(f"⏭️ Skipping migration: {file.name}")
            continue

        cursor = con.cursor()
        try:
            print(f"🔧 Running migration: {file.name}...")
            sql = file.read_text(encoding="utf-8")
            cursor.execute(sql)
            con.commit()

            mark_migration_as_applied(con, file.name)
            print(f"✅ Applied: {file.name}")

        except Exception as e:
            con.rollback()
            print(f"❌ Error running migration {file.name}: {e}")
            raise

        finally:
            cursor.close()

    print(f"📄 Found migrations: {[file.name for file in migration_files]}")
    print("🔥 All pending migrations processed.")
    migration_files = sorted(migrations_path.glob("*.sql"))
    print(f"📁 Migrations path: {migrations_path}")


if __name__ == "__main__":
    print("🚀 db_setup.py started")

    con = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT", 5432),
    )

    try:
        print("✅ Connected to database")
        run_migrations(con)
    finally:
        con.close()
        print("🔒 Connection closed")
