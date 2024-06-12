from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Starting bot'
        ),
        BotCommand(
            command='catalog',
            description='Demonstrate catalog'
        ),
        BotCommand(
            command='cancel',
            description='Cancelling action'
        ),
        BotCommand(
            command='basket',
            description='Showing basket'
        ),
        BotCommand(
            command='pay',
            description='Paying'
        ),
        BotCommand(
            command='contactus',
            description='Displaying contact info'
        ),
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
