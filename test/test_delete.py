from decimal import Decimal
from uuid import uuid4

from src.interfaces.Product_interfaces import IProduct
from src.services.product_service import ProductService


def test_product_delete():
    product_service = ProductService()

    product = IProduct(
        id=uuid4(),
        name=f"Mouse-{uuid4().hex[:8]}",
        price=Decimal("89.90"),
        quantity=10,
    )

    product_service.product_create(product)

    deleted = product_service.product_delete(product.name)

    assert deleted is True

    products = product_service.product_list()

    assert not any(item.id == product.id for item in products)


def test_product_delete_not_found():
    product_service = ProductService()

    deleted = product_service.product_delete(f"Nonexistent-{uuid4().hex}")

    assert deleted is False
