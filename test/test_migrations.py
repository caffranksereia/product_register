from database.conection import get_connection
from database.migration_runner import run_migrations


def main() -> None:
    con = get_connection()

    if con is None:
        print("Connection failed.")
        return

    try:
        run_migrations(con)
    finally:
        con.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
