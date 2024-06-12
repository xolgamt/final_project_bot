from aiogram import types
from aiogram.dispatcher import FSMContext


from handlers.basket import show_basket
from handlers.catalog import show_catalog
from handlers.contact import contact_us

from handlers.inlines.start_page import get_start_keyboard
from handlers.states.states import Catalog, MainMenu, Basket
from models import Client
from utils.database import SessionLocal


async def start_command_handler(message: types.Message, state: FSMContext):
    """Adds user to the database. Shows start menu inline"""

    await state.set_state(MainMenu.start_menu)
    start_keyboard = get_start_keyboard()
    await message.answer("Hello! Let's get ready for your next adventure together!")
    await message.answer("Please select an option:", reply_markup=start_keyboard)
    session = SessionLocal()
    user_id = message.from_user.id
    # Check if user already exists in clients table
    print(user_id)
    client = session.query(Client).filter_by(client_id=user_id).first()
    print(client)
    if not client:
        user_name = message.from_user.full_name
        user_address = None
        # Create client object
        client = Client(client_id=user_id,
                        client_name=user_name,
                        address=user_address)

        # Add client to database
        try:
            session.add(client)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error adding client to database: {e}")
            await message.answer("Error adding client to database. Please try again later.")
            return
        print(user_name)
    else:
        print(f"Client with id {user_id} already exists in database")


async def button_handler(callback_query: types.CallbackQuery, state: FSMContext):
    """Handler for start menu buttons"""

    prev_state = await state.get_state()
    print('starting on main menu buttons')
    print(prev_state)
    if callback_query.data == 'show_catalog':
        await show_catalog(callback_query.message, state)
    elif callback_query.data == 'delivery_info':
        await callback_query.message.answer('Delivery information:\n\n'
                                            'Our delivery service is provided by Nova Poshta or Meest.\n '
                                            'The estimated delivery time is 1-2 business days.\n '
                                            'The shipping cost for Nova Poshta is 50 UAH.\n'
                                            'The shipping cost for Meest is 60 UAH.\n')
    elif callback_query.data == 'payment_info':
        await callback_query.message.answer('Payment information:\n\n'
                                            'We accept Visa and Mastercard payments.\n '
                                            'You can also pay in cash upon delivery.\n'
                                            'If you prefer to pay upon delivery, please, '
                                            'contact us before placing your order.')
    elif callback_query.data == 'basket_view':
        await Basket.basket_view.set()
        await show_basket(callback_query, state)
    elif callback_query.data == 'contact_us':
        await callback_query.message.answer('If you have any questions, please, get in touch.')
        await contact_us(callback_query.message)
    elif callback_query.data == 'cancel':
        await state.finish()
        await start_command_handler(callback_query.message, state)
    else:
        await callback_query.message.answer('Not implemented yet')


