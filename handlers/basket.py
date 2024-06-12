from concurrent.futures import ThreadPoolExecutor

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from config import bot
from handlers.inlines.basket import basket_keyboard
from handlers.pay_delivery import process_pay
from handlers.states.states import Basket, MainMenu

from utils.database import get_product, get_user_basket, get_basket_items, delete_basket

# executor = ThreadPoolExecutor()


async def show_basket(callback_query: CallbackQuery, state: FSMContext):
    """Shows relevant information about client´s basket"""

    client_id = callback_query.from_user.id
    basket = await get_user_basket(client_id)

    if basket is None:
        await callback_query.answer("Your basket has no products yet.", show_alert=True, cache_time=2)
        await MainMenu.start_menu.set()
        return

    basket_items = await get_basket_items(basket)
    if not basket_items:
        await callback_query.answer("Your basket is empty.")
        await MainMenu.start_menu.set()
        return

    total_price = 0
    item_texts = []
    for item in basket_items:
        product_id = item['product_id']
        quantity = item['quantity']
        product = get_product(product_id)
        item_text = f"{product.product_name} ({product.brand}) x {quantity} = UAH{product.price * quantity:.2f}"
        total_price += product.price * quantity
        item_texts.append(item_text)

    message_text = "\n\n".join(item_texts) + f"\n\nTotal: UAH{total_price:.2f}"
    await Basket.basket_view.set()
    await state.update_data(basket_items=basket_items, total_price=total_price)
    # await callback_query.message.edit_text(message_text, reply_markup=basket_keyboard(basket_items))
    print(f'chat id from show_basket: {callback_query.from_user.id}')
    await bot.send_message(chat_id=callback_query.from_user.id,
                           text=message_text,
                           reply_markup=basket_keyboard(basket_items))



async def process_order(callback_query: CallbackQuery, state: FSMContext):
    """Processing the payment and order creation"""

    print('process order was called')
    previous_state = await state.get_state()
    print(f'previous_state from process_order: {previous_state}')
    user_id = callback_query.from_user.id  # Get the user id from the callback_query
    print(f'user_id from process_order: {user_id}')
    await process_pay(callback_query.message, user_id)

    await Basket.confirm_order.set()


# async def process_order(callback_query: types.CallbackQuery):
#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(executor, process_pay, callback_query.message)


async def clear_basket_handler(callback_query: CallbackQuery, state: FSMContext):
    # Delete the basket from the database
    delete_basket(client_id=callback_query.from_user.id)
    # Reset the state
    await state.reset_state()
    # Send a message to the user with the main menu options
    message_text = "Your basket has been cleared.\n\n"
    message_text += "Please, use /start command to go to the main menu"
    await callback_query.message.answer(message_text, reply_markup=None)













# @dp.message_handler(commands=['basket'])
# async def show_basket(message: Message, state: FSMContext):
#     # Get the user's basket from the state
#     session = SessionLocal()
#     user: User = message.from_user
#     user_id = user.id
#     print(user_id)
#     username = user.username
#     print(username)
#     print(user)
#     basket = await state.get_data()
#     print(basket)
#
#     if not basket:
#         await message.answer("Your basket is empty.\nYou can use /catalog command to take a look at our products")
#         return

    # Create a list of buttons for each item in the basket, including an option to remove each item
    # buttons = []
    # for item_id, item_data in basket.items():
    #     item = await Product.get_product_by_id(item_id)
    #     button_text = f"{item.name} - {item.price} x {item_data['quantity']}"
    #     remove_button = InlineKeyboardButton("Remove", callback_data=f"remove_item:{item_id}")
    #     buttons.append([InlineKeyboardButton(button_text, callback_data=f"basket_item:{item_id}"), remove_button])
    # # Create the inline keyboard with the list of items in the basket and an option to check out
    # checkout_button = InlineKeyboardButton("Checkout", callback_data="checkout")
    # keyboard = InlineKeyboardMarkup(buttons)
    # keyboard.add(checkout_button)
    # # Send the message with the list of items and the total price
    # total_price = sum(item_data['quantity'] * item.price for item_id, item_data in basket.items())
    # message_text = f"Your basket:\n\n{keyboard}\n\nTotal price: {total_price}"
    #
    # else:
    #     items = basket.items
    #     message = "Here are the items in your basket:\n\n"
    #     for item in items:
    #         product_id = item['product_id']
    #         quantity = item['quantity']
    #         product = session.query(Product).get(product_id)
    #         message += f"{product.product_name} ({product.brand}) - {quantity} x ${product.price}\n"
    #
    # update.message.reply_text(message)
    # for item in basket.items:
    #     print(item)
    #     # for
    #     # product_id = item['product_id'']
    #     # product=get_product(product_id)
    #     # product_name=product.product_name
    #     # product_quantity=item['quantity']
    #     #
    #     # message_text=f"Product: {product_name}, Quantity: {product['quantity']}, Price: {product['price']}")
    # message_text = "Your basket"
    # await message.answer(message_text)

# # Handler to process the selection of an item in the basket
# @dp.callback_query_handler(lambda c: c.data.startswith('basket_item:'), state=Basket.ITEM)
# async def process_basket_item(callback_query: CallbackQuery, state: FSMContext):
#     # Get the item id from the callback data
#     item_id = callback_query.data.split(':')[1]
#
#     # Update the state to the Basket.ITEM_QUANTITY state and pass the item id
#     await state.update_data(selected_item=item_id)
#     await Basket.ITEM_QUANTITY.set()
#
#     # Ask the user for the quantity of the selected item
#     item = await Product.get_product_by_id(item_id)
#     message_text = f"How many {item.name} would you like to add to your basket?"
#     await callback_query.message.answer(message_text)
#
# # Handler to process the quantity of an item selected in the basket
# @dp.message_handler(lambda message: message.text.isdigit(), state=Basket.ITEM_QUANTITY)
# async def process_item_quantity(message: Message, state: FSMContext):
#     # Get the selected item id and quantity from the state
#     data = await state.get_data()
#     item_id = data['selected_item']
#     quantity = int(message.text)
#
#     # Add the selected item to the user's basket in the state
#     basket = await state.get_data(default={})
#     if item_id in basket:
#         basket[item_id]['quantity'] += quantity
#     else:
#         basket[item_id] = {'quantity': quantity}
#     await state.set_data(basket)
#
#     # Update the state to the Basket.CATEGORY state
#     await Basket.CATEGORY.set()
#
#     # Show the basket to the user
#     await show_basket(message, state)
#
