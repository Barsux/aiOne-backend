from fastapi import APIRouter
from fastapi import Depends
from app.models.products import InputProduct, Product, ProductCategory
from app.services.products import ProductsService
from typing import List

router = APIRouter(
    prefix="/products"
)


@router.post("/")
def create_product(
    product: InputProduct,
    service: ProductsService = Depends()
) -> Product:
    return service.add_product(product)


@router.get("/")
def res_products(
    category: ProductCategory,
    page: int,
    service: ProductsService = Depends()
) -> List[Product]:
    return service.products_get_specified(category, page)


@router.get("/{product_id}}")
def get_product(
    product_id: int,
    service: ProductsService = Depends()
) -> Product:
    return service.get_product(product_id)


@router.get("/categories")
def get_categories(
    service: ProductsService = Depends()
) -> List[str]:
    return service.get_categories()


@router.get("/category")
def get_by_category(
    page: int,
    category: ProductCategory,
    service: ProductsService = Depends()
) -> List[Product]:
    return service.products_get_specified(category, page)


@router.put("/{product_id}")
def update_product(
    product_id: int,
    product: InputProduct,
    service: ProductsService = Depends()
) -> Product:
    return service.update_product(product_id, product)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    service: ProductsService = Depends()
):
    return service.delete_product(product_id)
