from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData
from config import bot
from handlers.inlines.catalog import get_categories_keyboard, get_products_keyboard, product_details_keyboard, \
    product_callback
from handlers.states.states import Catalog, MainMenu
from utils.database import SessionLocal, get_product, get_categories, get_products_by_category, add_item_to_basket, \
    get_user_basket, create_user_basket, get_item_count


async def cancel_command_handler(message: types.Message, state: FSMContext):
    """Cancels current command and conversation. Finishes the state"""

    current_state = await state.get_state()
    user_id = message.from_user.id
    if current_state is None:
        await message.answer("You don't have any active command to cancel.")
        return

    await state.finish()
    message.from_user.id = user_id
    await message.answer("Operation cancelled. What would you like to do next?\n "
                         "/start command will show you our main menu again", reply_markup=None)


goback_callback = CallbackData('goback', 'product_id', 'category_id')


async def show_catalog(message: types.Message, state: FSMContext):
    """Show all available categories for products"""

    print('show_catalog is called')
    previous_state = await state.get_state()
    print(f'previous state from show_catalog: {previous_state}')
    categories = get_categories()
    keyboard = get_categories_keyboard(categories)
    keyboard.add(InlineKeyboardButton('Back', callback_data=goback_callback.new(product_id=0, category_id=0)))
    await state.update_data(previous_state=previous_state, product_id=0, category_id=0)
    # await message.answer("Please, select a category:", reply_markup=keyboard)
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message.message_id, reply_markup=keyboard)
    await Catalog.categories_list.set()
    current_state = await state.get_state()
    print(f'current state from show_catalog: {current_state}')


async def show_products(callback_query: types.CallbackQuery, state: FSMContext, callback_data):
    """Show all available products for selected category"""

    print('show_products is called')
    previous_state = await state.get_state()
    print(f'previous state from show_products: {previous_state}')
    category_id = callback_data['category_id']
    await state.update_data(category_id=category_id)
    products = get_products_by_category(category_id)
    keyboard = get_products_keyboard(products, callback_data)
    keyboard.add(InlineKeyboardButton('Back', callback_data=goback_callback.new(product_id=0,
                                                                                  category_id=category_id)))
    await state.update_data(previous_state=previous_state, product_id=0, category_id=category_id)
    await bot.edit_message_reply_markup(chat_id=callback_query.message.chat.id,
                                        message_id=callback_query.message.message_id, reply_markup=keyboard)
    # await bot.send_message(chat_id=callback_query.message.chat.id, text="Please select a product:",
    #                        reply_markup=keyboard)
    await Catalog.products_list.set()
    await state.update_data(category_id=category_id)
    current_state = await state.get_state()
    print(f'current state from show_products: {current_state}')


async def show_product_details(callback_query: types.CallbackQuery, state: FSMContext):
    """Shows details of selected product: picture and description"""

    print('product_details is called')
    previous_state = await state.get_state()
    print(f'previous state from product_details: {previous_state}')
    data = product_callback.parse(callback_query.data)
    print(f'callback_query data for show_product_details: {data}')
    product_id = data['product_id']
    category_id = data['category_id']
    await state.update_data(product_id=product_id)
    product = get_product(product_id)
    if not product:
        await callback_query.message.answer("Sorry, this product is no longer available.")
        return
    keyboard = product_details_keyboard(int(product_id), int(category_id))

    keyboard.add(InlineKeyboardButton('Back', callback_data=goback_callback.new(product_id=product_id,
                                                                                  category_id=category_id)))
    await state.update_data(previous_state=previous_state, product_id=product_id, category_id=category_id)
    if product.photo is not None:
        photo_bytes = bytes(product.photo)
        await callback_query.message.answer("Here is product's description:")
        await callback_query.message.answer_photo(photo=photo_bytes,
                                                  caption=f"{product.product_name}\n\n"
                                                          f"Brand: {product.brand}\n"
                                                          f"Price: UAH{product.price}\n\n"
                                                          f"{product.description}", reply_markup=keyboard)
    else:
        await callback_query.message.answer(f"{product.product_name}\n\n"
                                            f"Brand: {product.brand}\n"
                                            f"Price: UAH{product.price}\n\n"
                                            f"{product.description}", reply_markup=keyboard)
    await Catalog.product_info.set()
    current_state = await state.get_state()
    print(f'current state from show_product-details: {current_state}')
    await state.update_data(product_id=product_id, category_id=product.category_id)


async def add_to_basket(callback_query: CallbackQuery, state: FSMContext):
    """Adds product to basket of the user"""

    print('add_to_basket is called')
    data = callback_query.data
    print(f'callback_query data for add_to_basket: {data}')
    product_id = int(data.split(":")[1])
    print(f"product_id: {product_id}")
    product = get_product(product_id)
    if product is None:
        print(f"Error: product with ID {product_id} not found")
        return
    print(f"product: {product}")
    client_id = callback_query.from_user.id
    print(f"client_id: {client_id}")
    basket = await get_user_basket(client_id)
    if basket is None:
        print(f"No basket found for client {client_id}; creating new basket")
        basket = create_user_basket(client_id)
    else:
        print(f"Found existing basket for client {client_id}: {basket}")
    await add_item_to_basket(client_id, product_id, product.price, quantity=1)

    item_count = await get_item_count(client_id, product_id)

    message_text = f"Product added to basket!\n " \
                   f"You have {item_count} unit(s) of this item in your basket."

    await callback_query.answer(message_text, show_alert=True, cache_time=2)
    # await state.reset_state()
    current_state = await state.get_state()
    print(current_state)
    # await Catalog.categories_list.set()




