import os
import secrets

from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, Depends, File, UploadFile
from fastapi.responses import FileResponse

from app import tables
from app.database import get_session
from app.settings import imagesdir as IMAGES_PATH
from app.models.products import Product, InputProduct, ProductCategory


class ProductsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def add_product(self, input_product: InputProduct):
        product = tables.Product()
        product.name = input_product.name
        product.description = input_product.description
        product.price = input_product.price
        product.category = input_product.category
        product.image_name = "NA"
        self.session.add(product)
        self.session.commit()
        return product

    def get_product(self, id: int) -> tables.Product:
        product = self.session.query(tables.Product).filter(tables.Product.id == id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден.")
        return product

    def update_product(self, id: int, product: InputProduct):
        product = self.get_product(id)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден.")
        for key, value in product.dict().items():
            setattr(product, key, value)
        self.session.commit()
        return product

    def delete_product(self, id: int):
        product = self.get_product(id)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден.")
        self.session.delete(product)
        self.session.commit()

    def product_set_image(self, id: int, file: UploadFile = File(...)) -> bool:
        product = self.get_product(id)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден.")
        product.image_name = secrets.token_urlsafe(32)
        path_to_image = os.path.join(IMAGES_PATH, product.image_name)
        try:
            with open(path_to_image, "wb") as out:
                out.write(file.file.read())
        except Exception:
            raise HTTPException(status_code=500, detail="Серверная ошибка. Невозможно сохранить файл.")
        self.session.commit()
        return True

    def product_get_image(self, id: int) -> FileResponse:
        product = self.get_product(id)
        if not product:
            raise HTTPException(status_code=404, detail="Товар не найден.")
        path_to_image = os.path.join(IMAGES_PATH, product.image_name)
        if not os.path.exists(path_to_image):
            raise HTTPException(status_code=404, detail="Изображение не найдено.")
        return path_to_image

    def products_get_all(self) -> List[Product]:
        products = self.session.query(tables.Product).all()
        return products

    def products_get_specified(self, category: ProductCategory, page: int) -> List[Product]:
        products = self.session.query(tables.Product).filter(tables.Product.category == category).offset(page * 10).limit(10).all()
        return products

    def products_get_page(self, page: int) -> List[Product]:
        products = self.session.query(tables.Product).offset(page * 10).limit(10).all()
        return products

    @classmethod
    def get_categories(cls) -> List[ProductCategory]:
        return [category.value for category in ProductCategory]