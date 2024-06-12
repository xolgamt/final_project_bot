import asyncio
from typing import Optional, Union, List, Type

from sqlalchemy import create_engine
from models import Order, Client, Basket
from models.base import Base
from sqlalchemy.orm import sessionmaker
from models.category import Category
from models.product import Product
from config import DB_URL
import json

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables
Base.metadata.create_all(bind=engine)


def create_category(category_name: str) -> Category:
    """Creating new category in categories table"""

    category = Category(category_name=category_name)
    with SessionLocal() as session:
        session.add(category)
        session.commit()
        session.refresh(category)
    return category


def create_product_pic(product_name, brand, description, price, category_id, quantity_available,
                       photo_url=None, photo=None):
    """Creating new product in products table"""

    with SessionLocal() as session:
        category = session.query(Category).filter(Category.category_id == category_id).first()
        if photo is not None:
            # Open image file
            with open(photo, 'rb') as f:
                # Read image data and assign it to the product photo field
                product_photo = f.read()
            # Create new product with binary photo
            product = Product(product_name=product_name, brand=brand, description=description, price=price,
                              photo=product_photo, quantity_available=quantity_available,
                              photo_url=photo_url, category_id=category_id)
        else:
            # Create new product without photo
            product = Product(product_name=product_name, brand=brand, description=description, price=price,
                              quantity_available=quantity_available,
                              photo_url=photo_url, category_id=category_id)

        session.add(product)
        session.commit()
        session.refresh(product)
    return product


def create_user_basket(client_id: int) -> Basket:
    """Creating new basket by client's id"""

    with SessionLocal() as session:
        basket = Basket(client_id=client_id)
        session.add(basket)
        session.commit()
        session.refresh(basket)
    return basket


def get_basket(client_id: int) -> Basket:
    """Retrieving client's basket by client's id"""

    with SessionLocal() as session:
        basket = session.query(Basket).filter(Basket.client_id == client_id).first()
    return basket


async def get_user_basket(client_id: int) -> Basket:
    """Retrieving client's basket by client's id. Async function"""

    with SessionLocal() as session:
        basket = await asyncio.to_thread(session.query(Basket).filter(Basket.client_id == client_id).first)
    return basket


# async def get_basket_items(basket: Basket) -> List:
#     with SessionLocal() as session:
#       return await asyncio.to_thread(basket.items)


async def get_basket_items(basket: Basket) -> List:
    """Retrieving basket items"""

    items = basket.items
    if isinstance(items, str):
        items = eval(items)
    return items


# def get_basket_items(basket: Basket) -> List:
#     session = SessionLocal()
#     return basket.products.all()


def delete_basket(client_id: Union[int, None]):
    """Deleting existing basket by client's id"""

    if client_id is None:
        raise ValueError("None value provided.")
    with SessionLocal() as session:
        client = session.query(Client).filter(Client.client_id == client_id).first()
        if client is not None and client.baskets:
            basket = client.baskets[0]  # assuming there is only one basket per client for now
            session.delete(basket)
            session.commit()



# async def delete_basket_async(client_id: Union[int, None]):
#     """Deleting existing basket by client's id. Async function"""
#     if client_id is None:
#         raise ValueError("None value provided.")
#     async with AsyncSession() as session:
#         async with session.begin():
#             client = await session.query(Client).filter(Client.client_id == client_id).first()
#             if client is not None and client.baskets:
#                 basket = client.baskets[0]  # assuming there is only one basket per client for now
#                 await session.delete(basket)
#                 await session.close()



async def add_item_to_basket(client_id: Union[int, None], product_id: Union[int, None], price: Union[float, None],
                  quantity: Union[int, None] = 1):
    """Adds new items to client´s basket. If there is no basket yet - creates it."""

    if None in [client_id, product_id, price]:
        raise ValueError("None value(s) provided.")
    with SessionLocal() as session:
        client = await asyncio.get_running_loop().run_in_executor(None,
                                                                  session.query(Client).filter(Client.client_id ==
                                                                                               client_id).first)
        if not client.baskets:
            basket = Basket()
            session.add(basket)
            client.baskets.append(basket)
            await asyncio.get_running_loop().run_in_executor(None, session.commit)
        else:
            basket = client.baskets[0]  # assuming there is only one basket per client for now
        item_dict = {"product_id": product_id, "quantity": quantity, "price": price}
        if basket.items:
            items_list = json.loads(basket.items)
        else:
            items_list = []
        item_exists = False
        for item in items_list:
            if item["product_id"] == product_id:
                item["quantity"] += quantity
                item_exists = True
                break
        if not item_exists:
            items_list.append(item_dict)
        basket.items = json.dumps(items_list)
        await asyncio.get_running_loop().run_in_executor(None, session.commit)


async def get_item_count(client_id: int, product_id: int) -> int:
    """Counts the number of items of the give product in client´s basket"""

    with SessionLocal() as session:
        basket = session.query(Basket).filter(Basket.client_id == client_id).first()
        if not basket:
            return 0
        items_list = json.loads(basket.items)
        item_count = sum(item["quantity"] for item in items_list if item["product_id"] == product_id)

    return item_count


def basket_total_value(basket_id: int) -> float:
    """Counts total monetary value of products in client´s basket"""

    with SessionLocal() as session:
        basket = session.query(Basket).filter(Basket.basket_id == basket_id).first()
        total = 0.00
        if basket.items:
            items_list = json.loads(basket.items)
            for item in items_list:
                total += item["price"] * item["quantity"]
    return total


def get_categories() -> list[Type[Category]]:
    """ Retrieve all the categories available. """

    with SessionLocal() as session:
        return session.query(Category).all()


def get_categories_names() -> List[Category]:
    """ Retrieve names of all the categories available. """

    with SessionLocal() as session:
        categories = session.query(Category.category_name).distinct().all()
        session.commit()
    return categories


def get_category_by_id(category_id: int) -> Optional[Category]:
    """ Retrieve a category by its unique identifier. """

    with SessionLocal() as session:
        category = session.query(Category).filter(Category.category_id == category_id).first()
    return category


def get_products_by_category(category_id: int) -> List[Product]:
    """Retrieve a list of products in a given category."""

    with SessionLocal() as session:
        return session.query(Product).join(Category).filter(Category.category_id == category_id).all()


def get_product_info(product_id: int) -> Optional[Product]:
    """ Retrieve information about a product by its unique identifier. """
    with SessionLocal() as session:
        return session.query(Product).filter(Product.product_id == product_id).first()


def get_product(product_id: int) -> Optional[Product]:
    """ Retrieve product by its unique identifier. """

    with SessionLocal() as session:
        product = session.query(Product).filter(Product.product_id == product_id).first()
    return product


def delete_category(category_id: int) -> bool:
    """ Delete a category by its unique identifier. """

    with SessionLocal() as session:
        category = session.query(Category).filter(Category.category_id == category_id).first()
        if category:
            session.delete(category)
            session.commit()
            return True
        return False


def delete_product(product_id: int) -> bool:
    """ Delete a product by its unique identifier. """

    with SessionLocal() as session:
        product = session.query(Product).filter(Product.product_id == product_id).first()
        if product:
            session.delete(product)
            session.commit()
            session.close()
            return True
        return False


def delete_order(order_id: int) -> bool:
    """ Delete an order by its unique identifier. """

    with SessionLocal() as session:
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if order:
            session.delete(order)
            session.commit()
            session.close()
            return True
        return False


