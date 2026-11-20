from database.conection import get_connection


def get_valid_connection():
    con = get_connection()

    if con is None:
        raise ConnectionError("Database connection failed.")

    return con
