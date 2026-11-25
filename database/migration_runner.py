from pathlib import Path

import psycopg2

MIGRATIONS_PATH = Path(__file__).resolve().parent / "migrations"


def ensure_schema_migrations_table(con) -> None:
    with con:
        with con.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    id BIGSERIAL PRIMARY KEY,
                    file_name VARCHAR(255) NOT NULL UNIQUE,
                    executed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """)

    print("✅ Migration control table ready.")


def get_applied_migrations(con) -> set[str]:
    with con.cursor() as cursor:
        cursor.execute("SELECT file_name FROM schema_migrations;")

        rows = cursor.fetchall()

    return {row[0] for row in rows}


def run_migrations(con) -> None:
    migrations_path = Path(__file__).resolve().parent.parent / "migrations"

    if not migrations_path.exists():
        raise FileNotFoundError(f"Migrations directory not found: {migrations_path}")

    ensure_schema_migrations_table(con)

    applied = get_applied_migrations(con)

    migration_files = sorted(migrations_path.glob("*.sql"))

    for file in migration_files:
        if file.name in applied:
            print(f"⏭️ Skipping migration: {file.name}")
            continue

        try:
            print(f"🔧 Running migration: {file.name}...")

            migration_sql = file.read_text(encoding="utf-8")

            with con:
                with con.cursor() as cursor:
                    cursor.execute(migration_sql)

                    cursor.execute(
                        """
                        INSERT INTO schema_migrations (file_name)
                        VALUES (%s);
                        """,
                        (file.name,),
                    )

            print(f"✅ Applied: {file.name}")

        except psycopg2.Error as error:
            print(f"❌ Migration failed: {file.name}: {error}")
            raise

    print("✅ All migrations processed.")
