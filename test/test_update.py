from decimal import Decimal
from uuid import uuid4

from src.interfaces.Product_interfaces import IProduct, IProductUpdate
from src.services.product_service import ProductService


def test_product_update():
    product_service = ProductService()

    product = IProduct(
        id=uuid4(),
        name="Keyboard",
        price=Decimal("150.00"),
        quantity=10,
    )

    product_service.product_create(product)

    product_update = IProductUpdate(
        name="Keyboard",
        new_name="Mechanical Keyboard",
        price=Decimal("250.00"),
        quantity=5,
    )

    updated = product_service.product_update(product_update)

    assert updated is True

    products = product_service.product_list()

    updated_product = next(item for item in products if item.id == product.id)

    assert updated_product.name == "Mechanical Keyboard"
    assert updated_product.price == Decimal("250.00")
    assert updated_product.quantity == 5
