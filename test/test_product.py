from decimal import Decimal
from uuid import uuid4

from database.get_connection import get_valid_connection
from src.interfaces.product_interface.product_interfaces import IProductUpdate
from src.services.product_service import ProductService


def test_product_update(test_product):
    service = ProductService()

    product_update = IProductUpdate(
        new_name="Updated Product",
        price=Decimal("15.90"),
        quantity=30,
    )

    updated = service.product_update(
        product_update,
        test_product["id"],
    )

    assert updated is True

    products = service.product_list()

    updated_product = next(
        (item for item in products if item.id == test_product["id"]),
        None,
    )

    assert updated_product is not None
    assert updated_product.name == "Updated Product"
    assert updated_product.price == Decimal("15.90")
    assert updated_product.quantity == 30


def test_product_delete(test_product):
    service = ProductService()

    deleted = service.product_delete(test_product["id"])

    assert deleted is True

    conn = get_valid_connection()

    if conn is None:
        raise ConnectionError("Database connection failed.")

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id
                FROM products
                WHERE id = %s;
                """,
                (str(test_product["id"]),),
            )

            product = cursor.fetchone()

        assert product is None

    finally:
        conn.close()


def test_product_delete_not_found():
    service = ProductService()

    deleted = service.product_delete(uuid4())

    assert deleted is False
