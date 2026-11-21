from uuid import UUID

from src.interfaces.sales.Sales_inteface import ISale
from src.services.sale_service import SaleService


def sale_product(product_id: UUID) -> None:
    sale_service = SaleService()

    try:
        quantity = int(input("Enter sale quantity: "))

        sale = ISale(
            product_id=product_id,
            quantity=quantity,
        )

        sale_id = sale_service.product_sale(sale)

        print("\nSale registered successfully!")
        print(f"Sale ID: {sale_id}")

    except ValueError as error:
        print(f"Error: {error}")

    except Exception as error:
        print(f"Unexpected error: {error}")
