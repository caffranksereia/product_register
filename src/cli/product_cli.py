from decimal import Decimal
from uuid import uuid4

from src.interfaces.Product_interfaces import IProduct, IProductUpdate
from src.services.product_service import ProductService


def register_product(product_service: ProductService) -> None:
    name = input("Product name: ")
    price = Decimal(input("Product price: "))
    quantity = int(input("Product quantity: "))

    product = IProduct(id=uuid4(), name=name, price=price, quantity=quantity)

    product_service.product_create(product)

    print("Product registered successfully!")


def list_products(product_service: ProductService) -> None:
    products = product_service.product_list()

    for product in products:
        print(f"{product.id} | {product.name} | {product.price} | {product.quantity}")


def update_product(product_service: ProductService) -> None:
    name = input("Enter product name: ")

    new_name = input("New product name: ")
    price = Decimal(input("New product price: "))
    quantity = int(input("New product quantity: "))

    product = IProductUpdate(
        name=name,
        new_name=new_name,
        price=price,
        quantity=quantity,
    )

    updated = product_service.product_update(product)

    if updated:
        print("Product updated successfully!")
    else:
        print("Product not found!")


def delete_product(product_service: ProductService) -> None:
    name = input("Enter product name to delete: ")

    product_service.product_delete(name)

    print("Product deleted successfully!")
