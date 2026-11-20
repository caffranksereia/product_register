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
        print("5 - Product Delete ")
        print("0 - Exit")

        option = input("Choose an option: ")

        if option == "1":
            product_service.product_create()

        elif option == "2":
            product_service.product_list()

        elif option == "3":
            product_service.product_update()

        elif option == "4":
            product_service.product_delete()

        elif option == "5":
            product_service.product_sale()

        elif option == "0":
            print("Exiting application...")
            break

        else:
            print("Invalid option!")
