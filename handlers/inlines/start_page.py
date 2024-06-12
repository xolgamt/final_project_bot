from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_start_keyboard() -> InlineKeyboardMarkup:
    """Creating inline keyboard for the starting page"""

    start_keyboard = InlineKeyboardMarkup(row_width=3, resize_keyboard=True)
    catalog_button = InlineKeyboardButton('\U0001F6CD Catalog', callback_data='show_catalog')
    delivery_info_button = InlineKeyboardButton('\U0001F69A Delivery Information',
                                                callback_data='delivery_info')
    payment_info_button = InlineKeyboardButton('\U0001F4B3 Payment Information',
                                               callback_data='payment_info')
    contact_us_button = InlineKeyboardButton('\U0001F4DE Contact Us',
                                             callback_data='contact_us')
    basket_button = InlineKeyboardButton('\U0001F6D2 Basket', callback_data='basket_view')

    start_keyboard.row(catalog_button, basket_button).\
        row(delivery_info_button, payment_info_button).\
        row(contact_us_button)
    return start_keyboard



