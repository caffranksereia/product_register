from pathlib import Path

from psycopg2 import Error

from database.conection import get_connection

EXPECTED_SKUS = (
    "MER-001",
    "MER-002",
    "MER-003",
    "MER-004",
    "MER-005",
    "MER-006",
    "MER-007",
    "MER-008",
    "MER-009",
    "MER-010",
)


def run_seed() -> None:
    con = get_connection()

    if con is None:
        raise ConnectionError("Could not connect to database.")

    seed_path = Path(__file__).resolve().parent.parent / "seeds" / "seed_products.sql"

    try:
        seed_sql = seed_path.read_text(encoding="utf-8")

        with con:
            with con.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM skus
                    WHERE code = ANY(%s);
                    """,
                    (list(EXPECTED_SKUS),),
                )

                existing_count = cursor.fetchone()

                if existing_count is not None:
                    if existing_count[0] == len(EXPECTED_SKUS):
                        print("⏭️ Products already registered.")
                        return

                print("🔧 Running product seed...")

                cursor.execute(seed_sql)

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM skus
                    WHERE code = ANY(%s);
                    """,
                    (list(EXPECTED_SKUS),),
                )

                result = cursor.fetchone()

                if result is not None:
                    print(f"✅ Registered products: {result[0]}/10")

    except (Error, OSError) as error:
        print(f"❌ Seed execution error: {error}")
        raise

    finally:
        con.close()
        print("🔒 Connection closed.")
