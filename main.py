from database.conection import get_connection
from database.db_setup import create_database
from database.migration_runner import run_migrations
from database.seed_runner import run_seed
from src.cli.cli import menu_registration


def initialize_database() -> bool:
    try:
        # 1. Create database if it does not exist
        create_database()

        # 2. Connect to database
        con = get_connection()

        if con is None:
            raise ConnectionError("Could not connect to database.")

        try:
            # 3. Run pending migrations
            run_migrations(con)

        finally:
            con.close()

        # 4. Insert initial data
        run_seed()

        print("✅ Database initialization completed.")
        return True

    except Exception as error:
        print(f"❌ Database initialization failed: {error}")
        return False


def main() -> None:
    if not initialize_database():
        print("Application startup canceled.")
        return
    menu_registration()


if __name__ == "__main__":
    main()
