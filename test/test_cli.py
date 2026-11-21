from decimal import Decimal
from uuid import uuid4

from src.interfaces.product_interface.product_interfaces import IProduct
from src.services.product_service import ProductService


def test_product_create_and_list():
    product_service = ProductService()

    product = IProduct(
        id=uuid4(), name="Mouse Logitech", price=Decimal("89.90"), quantity=10
    )

    created_product = product_service.product_create(product)

    assert created_product.id == product.id

    products = product_service.product_list()

    assert any(item.id == product.id for item in products)
