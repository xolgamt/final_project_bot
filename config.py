import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

PORTMONE_MERCHANT_ID = os.getenv('PORTMONE_MERCHANT_ID')
PORTMONE_SECRET_KEY = os.getenv('PORTMONE_SECRET_KEY')

PAY_TOKEN = os.getenv('PAYMENTS_TOKEN')

bot = Bot(token=os.environ.get('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)