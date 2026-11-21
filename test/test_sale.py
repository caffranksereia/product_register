from decimal import Decimal
from uuid import uuid4

import pytest

from database.get_connection import get_valid_connection
from src.interfaces.sales.Sales_inteface import ISale
from src.services.sale_service import SaleService


def test_product_sale(test_product):
    service = SaleService()

    sale = ISale(
        product_id=test_product["id"],
        quantity=2,
    )

    sale_id = service.product_sale(sale)

    assert sale_id is not None

    conn = get_valid_connection()

    if conn is None:
        raise ConnectionError("Database connection failed.")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT quantity
                FROM products
                WHERE id = %s;
                """,
                (str(test_product["id"]),),
            )
            stock_result = cursor.fetchone()

            cursor.execute(
                """
                SELECT total_value
                FROM sales
                WHERE id = %s;
                """,
                (str(sale_id),),
            )
            total_result = cursor.fetchone()

            cursor.execute(
                """
                SELECT quantity, unit_price, subtotal
                FROM sale_items
                WHERE sale_id = %s;
                """,
                (str(sale_id),),
            )
            item = cursor.fetchone()

        print("PRODUCT:", stock_result)
        print("SALE:", total_result)
        print("SALE ITEM:", item)

        assert stock_result is not None, "Product not found in database."
        assert total_result is not None, "Sale not found in sales."
        assert item is not None, "Sale item not found in sale_items."

        stock = stock_result[0]
        total = total_result[0]

        assert stock == 18
        assert total == Decimal("21.00")
        assert item[0] == 2
        assert item[1] == Decimal("10.50")
        assert item[2] == Decimal("21.00")

    finally:
        conn.close()


def test_product_sale_connection_failed(monkeypatch):
    monkeypatch.setattr(
        "src.services.sale_service.get_valid_connection",
        lambda: None,
    )

    service = SaleService()

    sale = ISale(
        product_id=uuid4(),
        quantity=1,
    )

    with pytest.raises(
        ConnectionError,
        match="Database connection failed.",
    ):
        service.product_sale(sale)


def test_product_sale_product_not_found():
    service = SaleService()

    sale = ISale(
        product_id=uuid4(),
        quantity=1,
    )

    with pytest.raises(ValueError, match="Product not found."):
        service.product_sale(sale)


def test_product_sale_insufficient_stock(test_product):
    service = SaleService()

    sale = ISale(
        product_id=test_product["id"],
        quantity=21,
    )

    with pytest.raises(
        ValueError,
        match="Insufficient product stock.",
    ):
        service.product_sale(sale)
