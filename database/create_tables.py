from database.conection import get_connection


def create_tables():
    con = get_connection()

    if con is None:
        raise ConnectionError("Could not connect to database.")

    try:
        with con, con.cursor() as cursor:
            with open("database/schema.sql", encoding="utf-8") as file:
                sql = file.read()

            cursor.execute(sql)

        print("Tables created successfully!")

    finally:
        con.close()


if __name__ == "__main__":
    create_tables()
