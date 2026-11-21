from src.cli.product_cli import delete_product, update_product
from src.cli.sales_cli import sale_product
from src.services.product_service import ProductService


def list_products(product_service: ProductService) -> None:
    while True:
        products = product_service.product_list()

        print("\n===================================")
        print("           PRODUCT LIST")
        print("===================================")

        if not products:
            print("No products registered.")
            return

        for index, product in enumerate(products, start=1):
            print(
                f"{index} - {product.name} | "
                f"R$ {product.price} | "
                f"Stock: {product.quantity}"
            )

        print("\n===================================")
        print("         PRODUCT OPERATIONS")
        print("===================================")
        print("1 - Update Product")
        print("2 - Delete Product")
        print("3 - Sale")
        print("0 - Back")

        option = input("\nChoose an option: ")

        if option == "0":
            break

        if option not in ("1", "2", "3"):
            print("Invalid option!")
            continue

        try:
            selection = int(input("Select product number: "))
        except ValueError:
            print("Invalid product number!")
            continue

        if selection < 1 or selection > len(products):
            print("Product not found!")
            continue

        product = products[selection - 1]

        if option == "1":
            update_product(product_service, product.id)

        elif option == "2":
            delete_product(product_service, product.id)

        elif option == "3":
            sale_product(product.id)
