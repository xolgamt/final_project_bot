from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from .base import Base

association_table = Table('product_basket_association', Base.metadata,
                          Column('product_id', Integer, ForeignKey('products.product_id')),
                          Column('basket_id', Integer, ForeignKey('baskets.basket_id'))
                          )


class Product(Base):
    """Product model"""
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    brand = Column(String, index=True)
    price = Column(Float, index=True)
    description = Column(String)
    photo_url = Column(String)
    photo = Column(LargeBinary)
    quantity_available = Column(Integer, default=0)

    category_id = Column(Integer, ForeignKey('categories.category_id'))

    category = relationship('Category', back_populates='products')

    # baskets = relationship('Basket', back_populates='product')
    baskets = relationship('Basket', secondary=association_table, back_populates='products', lazy='dynamic')

    # orders = relationship('Order', back_populates='product')

    def __repr__(self):
        return f'product_id {self.product_id}, ' \
               f'product_name {self.product_name}, ' \
               f'brand {self.brand}, ' \
               f'price UAH{self.price}'
