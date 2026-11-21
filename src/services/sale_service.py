from decimal import Decimal
from uuid import UUID, uuid4

from database.get_connection import get_valid_connection
from src.interfaces.sales.Sales_inteface import ISale


class SaleService:
    def product_sale(self, sale: ISale) -> UUID:
        conn = get_valid_connection()

        if conn is None:
            raise ConnectionError("Database connection failed.")

        try:
            with conn, conn.cursor() as cursor:
                # 1. Get product and lock its stock
                cursor.execute(
                    """
                    SELECT price, quantity
                    FROM products
                    WHERE id = %s
                    FOR UPDATE;
                    """,
                    (str(sale.product_id),),
                )

                product = cursor.fetchone()

                if product is None:
                    raise ValueError("Product not found.")

                unit_price = Decimal(product[0])
                stock = product[1]

                # 2. Check available stock
                if stock < sale.quantity:
                    raise ValueError("Insufficient product stock.")

                # 3. Calculate subtotal
                subtotal = unit_price * sale.quantity

                # 4. Generate sale ID
                sale_id = uuid4()

                # 5. Register sale
                cursor.execute(
                    """
                    INSERT INTO sales (id, total_value)
                    VALUES (%s, %s);
                    """,
                    (str(sale_id), subtotal),
                )

                # 6. Register sale item
                cursor.execute(
                    """
                    INSERT INTO sale_items (
                        id,
                        sale_id,
                        product_id,
                        quantity,
                        unit_price,
                        subtotal
                    )
                    VALUES (%s, %s, %s, %s, %s, %s);
                    """,
                    (
                        str(uuid4()),
                        str(sale_id),
                        str(sale.product_id),
                        sale.quantity,
                        unit_price,
                        subtotal,
                    ),
                )

                # 7. Update product stock
                cursor.execute(
                    """
                    UPDATE products
                    SET quantity = quantity - %s
                    WHERE id = %s;
                    """,
                    (sale.quantity, str(sale.product_id)),
                )

                return sale_id

        finally:
            conn.close()
