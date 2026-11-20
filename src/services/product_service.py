from database.get_connection import get_valid_connection
from src.interfaces.Product_interfaces import IProduct, IProductUpdate


class ProductService:
    def product_create(self, product: IProduct):
        conn = get_valid_connection()

        if conn is None:
            raise ConnectionError("Database connection failed.")

        try:
            with conn, conn.cursor() as cursor:
                cursor.execute(
                    """
                        INSERT INTO products (id, name, price, quantity)
                        VALUES (%s, %s, %s, %s)
                        """,
                    (str(product.id), product.name, product.price, product.quantity),
                )

            return product

        finally:
            conn.close()

    def product_list(self) -> list[IProduct]:
        conn = get_valid_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute("""
            SELECT id, name, price, quantity
            from products
            ORDER BY name;

        """)

                rows = cursor.fetchall()

                products = [
                    IProduct(id=row[0], name=row[1], price=row[2], quantity=row[3])
                    for row in rows
                ]

            return products

        finally:
            conn.close()

    def product_update(self, product: IProductUpdate) -> bool:
        conn = get_valid_connection()

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE products
                        SET name = %s, price = %s, quantity = %s
                        WHERE name = %s
                        """,
                        (
                            product.new_name,
                            product.price,
                            product.quantity,
                            product.name,
                        ),
                    )

                    return cursor.rowcount > 0

        finally:
            conn.close()

    def product_delete(self, name: str):
        conn = get_valid_connection()
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        DELETE FROM products
                        WHERE name = %s
                        """,
                        (name,),
                    )

                    return cursor.rowcount > 0

        finally:
            conn.close()


# Implementar


# def product_sale(self, product: IProduct, sale: ISale):
#     pass
