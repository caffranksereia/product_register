from uuid import uuid4

import pytest

from database.get_connection import get_valid_connection


@pytest.fixture
def test_product():
    product_id = uuid4()

    conn = get_valid_connection()

    if conn is None:
        raise ConnectionError("Database connection failed.")

    try:
        with conn, conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO products (id, name, price, quantity)
                VALUES (%s, %s, %s, %s);
                """,
                (str(product_id), "Pytest Product", 10.50, 20),
            )

        yield {
            "id": product_id,
            "name": "Pytest Product",
            "price": 10.50,
            "quantity": 20,
        }

    finally:
        cleanup_conn = get_valid_connection()

        if cleanup_conn is not None:
            try:
                with cleanup_conn, cleanup_conn.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT sale_id
                        FROM sale_items
                        WHERE product_id = %s;
                        """,
                        (str(product_id),),
                    )

                    sale_ids = [row[0] for row in cursor.fetchall()]

                    cursor.execute(
                        """
                        DELETE FROM sale_items
                        WHERE product_id = %s;
                        """,
                        (str(product_id),),
                    )

                    for sale_id in sale_ids:
                        cursor.execute(
                            """
                            DELETE FROM sales
                            WHERE id = %s;
                            """,
                            (str(sale_id),),
                        )

                    cursor.execute(
                        """
                        DELETE FROM products
                        WHERE id = %s;
                        """,
                        (str(product_id),),
                    )

            finally:
                cleanup_conn.close()
