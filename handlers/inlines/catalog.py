from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from models.product import Product
from models.category import Category


category_callback = CallbackData('category_name', 'category_id')
product_callback = CallbackData('product_name', 'product_id', 'category_id')
add_basket = CallbackData('product_name', 'product_id')


def get_categories_keyboard(categories: List[Category]) -> InlineKeyboardMarkup:
    """Creating inline keyboard for the list of categories"""

    cat_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    for category in categories:
        button = InlineKeyboardButton(category.category_name.replace('_', ' ').capitalize(),
                                      callback_data=category_callback.new(category_id=category.category_id))
        cat_keyboard.add(button)
    return cat_keyboard


def get_products_keyboard(products: List[Product], callback_data=None) -> InlineKeyboardMarkup:
    """Creating inline keyboard for the list of products"""

    prod_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    for product in products:
        button_text = f"{product.product_name} - UAH{product.price}"
        button = InlineKeyboardButton(button_text, callback_data=product_callback.new(product_id=product.product_id,
                                                                                      category_id=product.category_id))
        prod_keyboard.add(button)
    return prod_keyboard


def product_details_keyboard(product_id: int, category_id: int) -> InlineKeyboardMarkup:
    """Creating inline keyboard for the product´s details"""

    det_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    basket_button = InlineKeyboardButton(text='Add to Basket',
                                         callback_data=add_basket.new(product_id=product_id))
    det_keyboard.row(basket_button)
    return det_keyboard



