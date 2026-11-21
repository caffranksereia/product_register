from decimal import Decimal
from uuid import UUID, uuid4

from src.interfaces.product_interface.product_interfaces import IProduct, IProductUpdate
from src.services.product_service import ProductService


def register_product(product_service: ProductService) -> None:
    name = input("Product name: ")
    price = Decimal(input("Product price: "))
    quantity = int(input("Product quantity: "))

    product = IProduct(id=uuid4(), name=name, price=price, quantity=quantity)

    product_service.product_create(product)

    print("Product registered successfully!")


def update_product(
    product_service: ProductService,
    product_id: UUID,
) -> None:
    new_name = input("New product name: ")
    price = Decimal(input("New product price: "))
    quantity = int(input("New product quantity: "))

    product = IProductUpdate(
        new_name=new_name,
        price=price,
        quantity=quantity,
    )

    updated = product_service.product_update(product, product_id)

    if updated:
        print("Product updated successfully!")
    else:
        print("Product not found!")


def delete_product(
    product_service: ProductService,
    product_id: UUID,
) -> None:
    deleted = product_service.product_delete(product_id)

    if deleted:
        print("Product deleted successfully!")
    else:
        print("Product not found!")
