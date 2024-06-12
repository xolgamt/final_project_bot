from typing import List

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from models.product import Product


def basket_text(basket_items: List[dict]) -> str:
    """Creates the text to be used in basket description"""

    text = "Your basket:\n\n"
    total_price = 0
    for item in basket_items:
        product = Product.get_by_id(item['product_id'])
        quantity = item['quantity']
        price = product.price
        item_total = price * quantity
        total_price += item_total
        text += f"{product.product_name} ({product.brand}): {quantity} x UAH{price} = UAH{item_total}\n"
    text += f"\nTotal to pay: UAH{total_price}"
    return text


def basket_keyboard(basket_items) -> InlineKeyboardMarkup:
    """Creating inline keyboard for basket"""

    keyboard = InlineKeyboardMarkup(row_width=2)
    clear_button = InlineKeyboardButton(text="Clear basket", callback_data="clear_basket")
    keyboard.add(clear_button)
    keyboard.add(InlineKeyboardButton('Back to Main Menu', callback_data='cancel'))
    process_button = InlineKeyboardButton(text='Process Order', callback_data='process_order')
    keyboard.add(process_button)
    return keyboard



# def basket_keyboard(basket_items: List):
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     for item in basket_items:
#         product = get_product(item['product_id'])
#         quantity = item['quantity']
#         button_text = f"{product.product_name} ({product.brand})"
#         remove_callback_data = f"remove_basket_item_{product.product_id}"
#         minus_callback_data = f"minus_basket_item_{product.product_id}"
#         plus_callback_data = f"plus_basket_item_{product.product_id}"
#         button_row = [
#             InlineKeyboardButton(text="-", callback_data=minus_callback_data),
#             InlineKeyboardButton(text=str(quantity), callback_data='pass'),
#             InlineKeyboardButton(text="+", callback_data=plus_callback_data),
#             InlineKeyboardButton(text="Remove", callback_data=remove_callback_data),
#         ]
#         keyboard.add(*button_row)
#
#     clear_button = InlineKeyboardButton(text="Clear basket", callback_data="clear_basket")
#     keyboard.add(clear_button)
#     process_button = InlineKeyboardButton(text='Process Order', callback_data='process_order')
#     # process_button = InlineKeyboardButton(text='Process Order', callback_data='process_order')
#     keyboard.add(process_button)
#     return keyboard


#
# def basket_keyboard(basket_items: List):
#     keyboard = InlineKeyboardMarkup(row_width=2)
#     for item in basket_items:
#         product = get_product(item['product_id'])
#         quantity = item['quantity']
#         button_text = f"{product.product_name} ({product.brand}) - {quantity}"
#         callback_data = f"edit_basket_item_{product.product_id}"
#         button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
#         keyboard.add(button)
#
#         # Add buttons to increase and decrease quantity
#         increase_button = InlineKeyboardButton(text="+", callback_data=f"edit_basket_item_quantity_{product.product_id}_increase")
#         decrease_button = InlineKeyboardButton(text="-", callback_data=f"edit_basket_item_quantity_{product.product_id}_decrease")
#         keyboard.add(increase_button, decrease_button)
#
#     clear_button = InlineKeyboardButton(text="Clear basket", callback_data="clear_basket")
#     keyboard.add(clear_button)
#     process_button = InlineKeyboardButton(text='Process Order', callback_data='process_order')
#     keyboard.add(process_button)
#     return keyboard