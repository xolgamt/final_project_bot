import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import dp, bot

from aiogram.dispatcher.filters import Command, Text, Regexp
from aiogram.types import ContentType
from aiogram.utils import executor
from dotenv import load_dotenv

import config
from handlers.back import back_handler

from handlers.base import *
from handlers.basket import clear_basket_handler, process_order
from handlers.catalog import show_catalog, show_products, show_product_details, add_to_basket, cancel_command_handler
from handlers.contact import contact_us, handle_message, cancel_handler
from handlers.inlines.catalog import product_callback, category_callback, add_basket
from handlers.order import process_order_client
from handlers.pay_delivery import process_successful_payment, process_pay, process_pre_checkout_query, shipping_check
from handlers.start_page import *
from handlers.states.states import Catalog
from utils.commands import set_commands

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

load_dotenv()


# bot = Bot(token=os.environ.get('TOKEN'))
# storage = MemoryStorage()
# dp = Dispatcher(bot, storage=storage)


def register_message_handlers():
    dp.register_message_handler(cancel_command_handler, commands=['cancel'], state="*")
    dp.register_callback_query_handler(cancel_handler, lambda c: c.data == 'cancel', state="*")

    dp.register_callback_query_handler(back_handler, Regexp(r".*goback.*"), state="*")

    dp.register_message_handler(start_command_handler, commands=['start'], state="*")
    dp.register_callback_query_handler(button_handler, state=MainMenu.start_menu)

    dp.register_message_handler(show_catalog, commands=['catalog'], state="*")
    dp.register_callback_query_handler(show_products, category_callback.filter(), state=Catalog.categories_list)

    dp.register_callback_query_handler(show_product_details, product_callback.filter(), state=Catalog.products_list)

    dp.register_message_handler(show_basket, commands=['basket'], state='*')

    dp.register_callback_query_handler(show_basket, lambda c: c.data == 'basket')
    dp.register_callback_query_handler(add_to_basket, add_basket.filter(), state='*')
    dp.register_callback_query_handler(clear_basket_handler, lambda c: c.data == 'clear_basket', state='*')

    dp.register_message_handler(process_pay, commands=['pay'], state="*")
    dp.register_shipping_query_handler(shipping_check)
    dp.register_pre_checkout_query_handler(process_pre_checkout_query)
    dp.register_message_handler(process_successful_payment, content_types=[ContentType.SUCCESSFUL_PAYMENT])
    dp.register_callback_query_handler(process_order, lambda c: c.data == 'process_order', state=Basket.basket_view)

    dp.register_message_handler(contact_us, commands=['contactus'], state='*')
    dp.register_message_handler(handle_message)


if __name__ == '__main__':
    register_message_handlers()
    executor.start_polling(dp)
