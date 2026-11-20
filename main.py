from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    price: int
    quantity: int


class Sale(BaseModel):
    product_id: UUID
    quantity: int
    value: Decimal


class ProductService:
    def product_create(self):
        pass

    def product_list(self):
        pass

    def product_update(self):
        pass

    def product_delete(self):
        pass

    def product_sale(self):
        pass
