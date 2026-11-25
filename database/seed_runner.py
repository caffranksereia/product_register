from pathlib import Path

from psycopg2 import Error

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


SEED_PATH = Path(__file__).resolve().parent.parent / "seeds" / "seed_products.sql"


def run_seed(con) -> bool:
    if not SEED_PATH.exists():
        raise FileNotFoundError(f"Seed file not found: {SEED_PATH}")

    try:
        seed_sql = SEED_PATH.read_text(encoding="utf-8")

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

                result = cursor.fetchone()
                existing_count = result[0]

                if existing_count == len(EXPECTED_SKUS):
                    print("⏭️ Products already registered.")
                    return True

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
                registered_count = result[0]

                print(f"✅ Registered products: " f"{registered_count}/10")

                return True

    except (Error, OSError) as error:
        print(f"❌ Seed execution error: {error}")
        raise
