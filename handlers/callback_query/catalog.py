# from aiogram import types
# from aiogram.utils.callback_data import CallbackData
# from app.models import Category, Product
# from app.states import Catalog
# from app.keyboards.inline.catalog import product_keyboard
#
# category_callback = CallbackData('category', 'category_id')
#
# async def process_category(callback_query: types.CallbackQuery, state: FSMContext, callback_data: dict):
#     # Get the selected category
#     category_id = callback_data['category_id']
#     category = await Category.get(category_id)
#
#     # Get all the products in the selected category
#     products = await Product.query.filter_by(category_id=category.id).all()
#
#     # Create the inline keyboard with the list of products
#     keyboard = product_keyboard(products)
#
#     # Send the message with the list of products
#     await callback_query.message.answer("Please select a product:", reply_markup=keyboard)
#
#     # Set the current state to the Catalog.PRODUCT state
#     await Catalog.PRODUCT.set()
#
# async def process_product(callback_query: types.CallbackQuery, state: FSMContext):
#     # Get the selected product
#     product_id = callback_query.data.split(":")[1]
#     product = await Product.get(product_id)
#
#     # Create the inline keyboard with the Add to Basket button
#     keyboard = InlineKeyboardMarkup()
#     button = InlineKeyboardButton("Add to Basket", callback_data=f"add_to_basket:{product_id}")
#     keyboard.add(button)
#
#     # Send the message with the product details and the Add to Basket button
#     message_text = f"Product: {product.name}\nPrice: {product.price}\nDescription: {product.description}\n\n"
#     await callback_query.message.answer(message_text, reply_markup=keyboard)




# async def button_handler(callback: types.CallbackQuery, state: FSMContext):
#     if callback.data == 'show_catalog':
#         await show_catalog(callback.message, state)
# #
# # @dp.callback_query_handler(category_callback.filter())
# async def show_products_by_category(query: CallbackQuery, callback_data: dict, state: FSMContext):
#     # Get the category ID from the callback data
#     category_id = int(callback_data.get("category_id"))
#     # Get all products that belong to the selected category
#     session = SessionLocal()
#
#     product_callback = CallbackData("product_name", "product_id")
#     products = session.query(Product).filter(Product.category_id == category_id).all()
#     session.close()
#     # Create a keyboard with all product buttons
#     keyboard = get_products_keyboard(products)
#     # Edit the message to display the products and the product keyboard
#     await query.message.edit_text("Please select a product:", reply_markup=keyboard)
#     # Switch to the PRODUCT state to handle the user's next message
#     await Catalog.PRODUCT.set()
#
# # Handler for when a user selects a product button
# # @dp.callback_query_handler(product_callback.filter())
# async def show_product_details(query: CallbackQuery, callback_data: dict, state: FSMContext):
#     # Get the product ID from the callback data
#     product_id = int(callback_data.get("product_id"))
#
#     # Get the product details from the database
#     session = SessionLocal()
#     product = session.query(Product).filter_by(id=product_id).first()
#     session.close()
#
#     # Send a message to the user with the product details
#     await query.message.answer(f"Product name: {product.name}\nPrice: {product.price}\nDescription: {product.description}")
#
#     # End the conversation by resetting the state
#     await state.finish()
#
# #
# # # @dp.callback_query_handler(lambda c: c.data.startswith("category:"), state=Catalog.CATEGORY)
# async def process_category(callback_query: types.CallbackQuery, state: FSMContext):
#     print("process_catalog function called")
#     # Get the selected category
#     category_id = callback_query.data.split(":")[1]
#     session = SessionLocal()
#     category = session.query(Category).get(category_id)
#     # category = await Category.get(category_id)
#     # Get all the products in the selected category
#     products = await Product.query.filter_by(category_id=category.category_id).all()
#     # Create the inline keyboard with the list of products
#     keyboard = get_products_keyboard(products)
#     # Send the message with the list of products
#     await callback_query.message.answer("Please select a product:", reply_markup=keyboard)
#     # Set the current state to the Catalog.PRODUCT state
#     await Catalog.PRODUCT.set()
#
# # @dp.callback_query_handler(lambda c: c.data.startswith("product:"), state=Catalog.PRODUCT)
# async def process_product(callback_query: types.CallbackQuery, state: FSMContext):
#     # Get the selected product
#     product_id = callback_query.data.split(":")[1]
#     session = SessionLocal()
#     product = session.query(Product).get(product_id)
#     # product = await Product.get(product_id)
#     # Create the inline keyboard with the Add to Basket button
#     keyboard = InlineKeyboardMarkup()
#     button = InlineKeyboardButton("Add to Basket", callback_data=f"add_to_basket:{product_id}")
#     keyboard.add(button)
#     # Send the message with the product details and the Add to Basket button
#     message_text = f"Product: {product.product_name}\n" \
#                    f"Brand: {product.brand}\n" \
#                    f"Price: {product.price}\n" \
#                    f"Description: {product.description}\n\n"
#     await callback_query.message.answer(message_text, reply_markup=keyboard)
#     # Set the current state back to the Catalog.CATEGORY state
#     await Catalog.CATEGORY.set()