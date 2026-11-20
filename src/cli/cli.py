from src.cli.product_cli import (
    delete_product,
    list_products,
    register_product,
    update_product,
)
from src.services.product_service import ProductService


def menu_registration() -> None:
    product_service = ProductService()
    while True:
        print("\n===================================")
        print("\n         PORDUCT REGISTRATION       ")
        print("\n===================================")
        print("1 -  Product Register")
        print("2 - Product List")
        print("3 - Product Update")
        print("4 - Product Delete ")
        print("5 - Sale ")
        print("0 - Exit")

        option = input("Choose an option: ")

        if option == "1":
            register_product(product_service)

        elif option == "2":
            list_products(product_service)

        elif option == "3":
            update_product(product_service)

        elif option == "4":
            delete_product(product_service)

        elif option == "5":
            delete_product(product_service)

        elif option == "0":
            print("Exiting application...")
            break

        else:
            print("Invalid option!")
