from src.cli.list_product_cli import list_products
from src.cli.product_cli import (
    register_product,
)
from src.services.product_service import ProductService


def menu_registration() -> None:
    product_service = ProductService()
    while True:
        print("\n===================================")
        print("\n         PRODUCT REGISTRATION       ")
        print("\n===================================")
        print("1 -  Product Register")
        print("2 - Product List")
        print("0 - Exit")

        option = input("Choose an option: ")

        if option == "1":
            register_product(product_service)

        elif option == "2":
            list_products(product_service)

        elif option == "0":
            print("Exiting application...")
            break

        else:
            print("Invalid option!")
