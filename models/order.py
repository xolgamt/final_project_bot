from sqlalchemy import Column, Integer, String, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship

from .base import Base


class Order(Base):
    """Order model"""
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id"))
    # basket_id = Column(Integer, ForeignKey("baskets.basket_id"))
    items = Column(JSON)
    total_price = Column(Float, index=True)
    delivery_method = Column(String)
    delivery_address = Column(String)
    status = Column(String)

    client = relationship("Client", back_populates="orders")
    # basket = relationship("Basket", back_populates="order")
    # basket_fk = ForeignKey("baskets.basket_id")


    def __repr__(self):
        return f'Order(order_id={self.order_id}, client_id={self.client_id}, total_price={self.total_price})'

    # def create(self, session):
    #     product = session.query(Product).filter_by(product_id=self.product_id).first()
    #     if product is None:
    #         raise ValueError("Invalid product ID")
    #
    #     if product.quantity_available < self.quantity:
    #         raise ValueError("Not enough quantity available")
    #
    #     product.quantity_available -= self.quantity
    #     self.total_price = product.price * self.quantity
    #
    #     session.add(self)
    #     session.commit()