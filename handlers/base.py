from aiogram import types


async def send_hello(message: types.Message):
    await message.reply('Hello! This is GoAdventure Bot. Let´s get ready for your next adventure together!')


async def send_help(message: types.Message):
    await message.reply('Hello! This is GoAdventure Bot. Let´s get ready for your next adventure together!')


async def echo(message: types.Message):
    await message.answer(message.text)

