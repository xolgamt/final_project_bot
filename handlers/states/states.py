from aiogram.dispatcher.filters.state import State, StatesGroup


class MainMenu(StatesGroup):
    start_menu = State()


class Catalog(StatesGroup):
    categories_list = State()
    products_list = State()
    product_info = State()


class Basket(StatesGroup):
    basket_view = State()
    confirm_order = State()


