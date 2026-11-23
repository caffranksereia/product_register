from src.setup.project_setup import restart_in_venv, setup_project


def main() -> None:
    try:
        # 1. Prepare project environment
        setup_project()

        # 2. Restart inside virtual environment
        restart_in_venv()

        # Imports only after environment activation
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

        # 3. Initialize database
        if not initialize_database():
            print("Application startup canceled.")
            return

        # 4. Start application
        menu_registration()

    except Exception as error:
        print(f"❌ Application startup failed: {error}")


if __name__ == "__main__":
    main()
