from sqlalchemy import Column, Integer, ForeignKey, JSON, BigInteger
from sqlalchemy.orm import relationship

from .base import Base
from .product import association_table


class Basket(Base):
    """Basket model"""
    __tablename__ = 'baskets'

    basket_id = Column(Integer, primary_key=True, index=True)
    items = Column(JSON)
    # quantity = Column(Integer, index=True)
    # product_id = Column(Integer, ForeignKey('products.product_id'))
    # product = relationship('Product', back_populates='baskets')

    client_id = Column(BigInteger, ForeignKey('clients.client_id'), unique=True)
    client = relationship('Client', back_populates='baskets')
    products = relationship('Product', secondary=association_table, back_populates='baskets', lazy='dynamic')
    # order = relationship('Order', uselist=False, back_populates='basket')

    def __repr__(self):
        return f'Basket(basket_id={self.basket_id}, items={self.items}, client_id={self.client_id})'