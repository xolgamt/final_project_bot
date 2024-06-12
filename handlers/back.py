from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from handlers.catalog import show_catalog, show_products, goback_callback
from handlers.start_page import start_command_handler
from handlers.states.states import MainMenu, Catalog


async def back_handler(callback_query: CallbackQuery, state: FSMContext):
    """Moves one step back in the catalog navigation"""

    print('back_handler is called')
    current_state = await state.get_state()
    print(current_state)
    if 'product_info' in current_state:
        print('going back from product_info')
        await state.set_state(Catalog.products_list)
        new_state = await state.get_state()
        print(f'setting new state: {new_state}')
        data = goback_callback.parse(callback_query.data)
        product_id = data['product_id']
        category_id = data['category_id']
        await state.update_data(product_id=product_id, category_id=category_id)
        print(f'callback_query data for back_handler: {data}')
        callback_data = {'category_id': category_id}
        await show_products(callback_query, state, callback_data)

    elif 'products_list' in current_state:
        print('going back from products_list')
        await state.set_state(Catalog.categories_list)
        new_state = await state.get_state()
        print(f'setting new state: {new_state}')
        await show_catalog(callback_query.message, state)

    elif 'categories_list' in current_state:
        await state.set_state(MainMenu.start_menu)
        new_state = await state.get_state()
        print(f'setting new state: {new_state}')
        await start_command_handler(callback_query.message, state)