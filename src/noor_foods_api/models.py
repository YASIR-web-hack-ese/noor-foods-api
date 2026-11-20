from datetime import date
from decimal import Decimal
from typing import Annotated, Any

from pydantic import StringConstraints
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel

ProductName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2),
]


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    category_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=Text, min_length=2, unique=True)


class Supplier(SQLModel, table=True):
    __tablename__ = "suppliers"

    supplier_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=Text, min_length=2)


class ProductBase(SQLModel):
    name: ProductName = Field(sa_type=Text)
    category_id: int = Field(foreign_key="categories.category_id")
    supplier_id: int = Field(foreign_key="suppliers.supplier_id")
    unit_price: Decimal = Field(max_digits=10, decimal_places=2, gt=0)
    stock_quantity: int = Field(default=0, ge=0)
    is_discontinued: bool = False
    attributes: dict[str, Any] = Field(default_factory=dict, sa_type=JSONB)


class Product(ProductBase, table=True):  # pyright: ignore[reportCallIssue]
    __tablename__ = "products"

    product_id: int | None = Field(default=None, primary_key=True)
    sku: str = Field(sa_type=Text, unique=True)
    added_on: date = Field(default_factory=date.today)


class ProductCreate(ProductBase):
    sku: str = Field(min_length=3)


class ProductUpdate(SQLModel):
    name: ProductName | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    unit_price: Decimal | None = Field(
        default=None, max_digits=10, decimal_places=2, gt=0
    )
    stock_quantity: int | None = Field(default=None, ge=0)
    is_discontinued: bool | None = None
    attributes: dict[str, Any] | None = None


class ProductRead(ProductBase):
    product_id: int
    sku: str
    added_on: date
