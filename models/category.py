from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import asc
from .base import Base


class Category(Base):
    """Category model"""
    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String, index=True)

    products = relationship('Product', back_populates='category')

    # @classmethod
    # def get_query(cls, session: Session):
    #     return session.query(cls).order_by(asc(cls.category_name))
