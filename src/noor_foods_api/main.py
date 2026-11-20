from typing import Annotated

from fastapi import FastAPI, Query, Response, status

from . import crud
from .dependencies import ProductDep, SessionDep
from .models import Category, Product, ProductCreate, ProductRead, ProductUpdate

app = FastAPI(
    title="Noor Foods API",
    description="Products, orders and stock for Noor Foods.",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "Noor Foods API", "docs": "/docs"}


@app.get("/categories")
def list_categories(session: SessionDep) -> list[Category]:
    return crud.list_categories(session)


@app.get("/products", response_model=list[ProductRead])
def list_products(
    session: SessionDep,
    category_id: int | None = None,
    search: str | None = None,
    in_stock: bool | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[Product]:
    return crud.list_products(
        session,
        category_id=category_id,
        search=search,
        in_stock=in_stock,
        limit=limit,
        offset=offset,
    )


@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(product: ProductDep) -> Product:
    return product


@app.post(
    "/products",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
)
def create_product(payload: ProductCreate, session: SessionDep) -> Product:
    return crud.create_product(session, payload)


@app.patch("/products/{product_id}", response_model=ProductRead)
def update_product(
    product: ProductDep, payload: ProductUpdate, session: SessionDep
) -> Product:
    return crud.update_product(session, product, payload)


@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product: ProductDep, session: SessionDep) -> Response:
    crud.delete_product(session, product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
