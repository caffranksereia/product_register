from decimal import Decimal, InvalidOperation
from uuid import UUID, uuid4

from src.interfaces.product_interface.product_interfaces import IProduct, IProductUpdate
from src.services.product_service import ProductService


def register_product(product_service: ProductService) -> None:
    try:
        name = input("Product name: ")
        price = Decimal(input("Product price: "))
        quantity = int(input("Product quantity: "))

        validate_product(name, price, quantity)

        product = IProduct(
            id=uuid4(),
            name=name,
            price=price,
            quantity=quantity,
        )

        product_service.product_create(product)

        print("Product registered successfully!")

    except (ValueError, TypeError, InvalidOperation) as error:
        print(f"Error: {error}")
        print("Product was not registered.")


def validate_product(name, price, quantity):
    if not isinstance(name, str) or not name.strip():
        raise ValueError("Invalid product name.")

    if not isinstance(price, Decimal):
        raise TypeError("Price must be a Decimal.")

    if not price.is_finite() or price <= Decimal("0"):
        raise ValueError("Price must be greater than zero.")

    if type(quantity) is not int:
        raise TypeError("Quantity must be an integer.")

    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero.")

    return True


def update_product(
    product_service: ProductService,
    product_id: UUID,
) -> None:
    new_name = input("New product name: ")
    price = Decimal(input("New product price: "))
    quantity = int(input("New product quantity: "))

    validate_product(new_name, price, quantity)

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
