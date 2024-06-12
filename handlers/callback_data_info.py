from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData


class ProductInfo(CallbackData):
    product_id: str
    product_name: str
    brand: str
    price: int
    description: str
    photo: str
    category_id: int
