from database.conection import get_connection


def main() -> None:
    con = get_connection()

    if con is None:
        print("Connection failed.")
        return

    try:
        with con.cursor() as cursor:
            cursor.execute("SELECT current_database();")
            result = cursor.fetchone()

            if result is not None:
                print(f"Database connected: {result[0]}")
            else:
                print("No database returned.")

    finally:
        con.close()
        print("Connection closed.")


if __name__ == "__main__":
    main()
