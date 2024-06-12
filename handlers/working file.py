# async def show_products(callback_query: types.CallbackQuery, state: FSMContext, callback_data):
#     """Show all available products for selected category"""
    # print('show_products is called')
    # previous_state = await state.get_state()
    # print(f'previous state from show_products: {previous_state}')
    # data = category_callback.parse(callback_query.data)
    # print(f'callback_query data for show_products: {data}')
    # category_id = data['category_id']
    # await state.update_data(category_id=category_id)
    # products = get_products_by_category(category_id)
    # keyboard = get_products_keyboard(products)
    # await callback_query.message.edit_text("Please select a product:")
    # await callback_query.message.edit_reply_markup(keyboard)
    # await Catalog.products_list.set()
    # await state.update_data(category_id=category_id)
    # current_state = await state.get_state()
    # print(f'current state from show_products: {current_state}')


# async def back_to_categories(callback_query: types.CallbackQuery, state: FSMContext):
#     await state.set_state(Catalog.categories_list)
#     await callback_query.message.edit_reply_markup(reply_markup=None)
#     await callback_query.message.edit_text("We offer these types of products.\n Please select an option:")
#     session = SessionLocal()
#     categories = session.query(Category).all()
#     session.close()
#     await callback_query.message.edit_reply_markup(reply_markup=get_categories_keyboard(categories))

#

# async def back_to_products_list(callback_query: CallbackQuery, callback_data: dict):
#     category_id = callback_data.get("category_id")
#     print(category_id)
#     category = get_category_by_id(category_id)
#
#     if category is None:
#         await callback_query.answer()
#         return
#
#     session = SessionLocal()
#     products = session.query(Product).filter(Product.category_id == category_id).all()
#     session.close()
#     if not products:
#         await callback_query.message.answer("No products found for this category.")
#         return
#
#     products_keyboard = product_details_keyboard(products, category_id)
#     categories_keyboard = get_categories_keyboard()
#
#     markup = InlineKeyboardMarkup(row_width=2)
#     markup.add(*products_keyboard)
#     markup.add(*categories_keyboard)
#
#     if callback_query.message:
#         await callback_query.message.edit_text("Here are available products in picked category:", reply_markup=markup)
#     else:
#         await callback_query.answer()

# async def back_to_products_list(callback_query: types.CallbackQuery, state: FSMContext):
#     print('back_to_product_list is called')
#     data = back_callback.parse(callback_query.data)
#     print(data)
#     product_id = data['product_id']
#     print(product_id)
#     category_id = data['category_id']
#     print(category_id)
#     await Catalog.products_list.set()
#     callback_query.data = category_callback
#     await state.update_data(category_id=category_id)
#     # await show_products(callback_query, state)
#     session = SessionLocal()
#     products = session.query(Product).filter(Product.category_id == category_id).all()
#     session.close()
#     # await callback_query.message.edit_caption(caption="", reply_markup=None)
#     await callback_query.message.answer("Here are available products in picked category:")
#     keyboard = get_products_keyboard(products)
#     await callback_query.message.edit_reply_markup(keyboard)
#     await Catalog.products_list.set()
#     await state.update_data(category_id=category_id)

# back_callback = CallbackData('back_to_products_list', 'product_id', 'category_id')
# category_callback = CallbackData('category_name', 'category_id')
# product_callback = CallbackData('product_name', 'product_id', 'category_id')
# add_basket = CallbackData('product_name', 'product_id')
#
#
# def get_categories_keyboard(categories: List[Category]) -> InlineKeyboardMarkup:
#     """Creating inline keyboard for the list of categories"""
#
#     cat_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
#     for category in categories:
#         button = InlineKeyboardButton(category.category_name.replace('_', ' ').capitalize(),
#                                       callback_data=category_callback.new(category_id=category.category_id))
#         cat_keyboard.add(button)
#     cat_keyboard.add(InlineKeyboardButton('Back', callback_data='cancel'))
#     return cat_keyboard
#
#
# def get_products_keyboard(products: List[Product], callback_data=None) -> InlineKeyboardMarkup:
#     """Creating inline keyboard for the list of products"""
#
#     prod_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
#     for product in products:
#         button_text = f"{product.product_name} - UAH{product.price}"
#         button = InlineKeyboardButton(button_text, callback_data=product_callback.new(product_id=product.product_id,
#                                                                                       category_id=product.category_id))
#         prod_keyboard.add(button)
#     prod_keyboard.add(InlineKeyboardButton(text='Back', callback_data='back_to_categories'))
#     return prod_keyboard
#
#
# def product_details_keyboard(product_id: int, category_id: int) -> InlineKeyboardMarkup:
#     """Creating inline keyboard for the product´s details"""
#
#     det_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
#     basket_button = InlineKeyboardButton(text='Add to Basket',
#                                          callback_data=add_basket.new(product_id=product_id))
#     det_keyboard.row(basket_button)
#     det_keyboard.add(InlineKeyboardButton(text='Back',
#                                           callback_data=back_callback.new(product_id=product_id, category_id=category_id)))
#
#     return det_keyboard

####----------------------------------------------
# from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
# from aiogram import types
#
# from bot import dp
#
# products_info_button = InlineKeyboardButton(text='Learn about products', callback_data='products_info')
# button2 = InlineKeyboardButton(text='Help', callback_data='send_help')
# keyboard_inline = InlineKeyboardMarkup().add(products_info_button, button2)
#
# product1_button = InlineKeyboardButton(text='Product 1', callback_data='product_1')
# product2_button = InlineKeyboardButton(text='Product 2', callback_data='product_2')
# product3_button = InlineKeyboardButton(text='Product 3', callback_data='product_3')
# products_keyboard_inline = InlineKeyboardMarkup().row(product1_button, product2_button, product3_button)
#
#
# @dp.message_handler(commands=['hello'])
# async def hello(message: types.Message):
#     await message.reply('What would you like to do?', reply_markup=keyboard_inline)
#
# @dp.callback_query_handler(text=['products_info', 'send_help'])
# async def starter(call:types.CallbackQuery):
#     if call.data == 'products_info':
#         await call.message.answer('Pick the category', reply_markup=products_keyboard_inline)
#     if call.data.startswith('start_'):
#         await call.message.answer('Choose an option:', reply_markup=products_keyboard_inline)
#     if call.data == 'send_help':
#         await call.message.answer('help')
#     await call.answer()
#
# @dp.callback_query_handler(text=['product_1', 'product_2', 'product_3'])
# async def handle_products_button(call: types.CallbackQuery):
#     if call.data == 'product_1':
#         await call.message.answer('You pressed Product 1')
#     elif call.data == 'product_2':
#         await call.message.answer('You pressed Product 2')
#     elif call.data == 'product_3':
#         await call.message.answer('You pressed Product 3')
#     await call.answer()
