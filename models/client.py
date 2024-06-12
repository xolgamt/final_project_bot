from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from .base import Base

class Client(Base):
    """Client model"""
    __tablename__ = 'clients'

    client_id = Column(BigInteger, primary_key=True, index=True)
    client_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    phone = Column(String, unique=True, index=True, nullable=True)
    address = Column(String, index=True, nullable=True)

    orders = relationship('Order', back_populates='client')
    baskets = relationship('Basket', back_populates='client')