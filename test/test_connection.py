from database.conection import get_connection


def test_database_connection():
    print("Iniciando teste...")

    con = get_connection()

    print("Conexão retornada:", con)

    assert con is not None

    cursor = con.cursor()

    try:
        cursor.execute("SELECT 1")
        result = cursor.fetchone()

        print("Resultado SQL:", result)

        assert result[0] == 1

        print("PostgreSQL conectado com sucesso!")

    finally:
        cursor.close()
        con.close()


if __name__ == "__main__":
    test_database_connection()
