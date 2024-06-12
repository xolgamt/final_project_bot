from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import bot
from handlers.inlines.start_page import get_start_keyboard
from handlers.states.states import MainMenu


async def contact_us(message: types.Message):
    # Create the contact us form
    form = InlineKeyboardMarkup(row_width=1)
    form.add(
        InlineKeyboardButton('Email', url='mailto:goadventure.ec@gmail.com'),  # mailto:your_email@example.com
        InlineKeyboardButton('Telegram', url='https://t.me/go_adventure_bot'),  # https://t.me/your_bot
        InlineKeyboardButton('WhatsApp', url='https://wa.me/+380631234567'),
        InlineKeyboardButton('Cancel', callback_data='cancel')
    )

    # Send the contact us form to the user
    await message.answer('Please select how you want to contact us:', reply_markup=form)


async def handle_message(message: types.Message):
    # Forward the message to your email address
    await bot.send_message('goadventure.ec@gmail.com', f'New message from {message.chat.first_name}:\n\n{message.text}')
    await message.answer('Thank you for your message! We will get back to you as soon as possible.')


async def cancel_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await state.set_state(MainMenu.start_menu)
    await callback_query.message.edit_reply_markup(reply_markup=None)
    await callback_query.message.edit_text("Canceled. Please select an option:")
    await callback_query.message.edit_reply_markup(reply_markup=get_start_keyboard())
