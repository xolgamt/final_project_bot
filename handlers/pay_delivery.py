from aiogram import types
from aiogram.types import ShippingOption, LabeledPrice, ShippingQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config import PAY_TOKEN, bot
from models import Order, Client
from utils.database import basket_total_value, get_user_basket, SessionLocal, get_basket, delete_basket


pic_link = 'https://devathon.com/wp-content/uploads/2020/02/Top-10-Payment-Gateways-Devathon.png'


async def process_pay(message: types.Message, user_id=None):
    """Processes order payment and creates an order from the basket"""

    print('process_pay is called')
    if PAY_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'Order Payment.\n'
                                                'If you changed your mind just enter /cancel command.\n')
    print(f' user_id from process_pay {message.from_user.id}')
    print(message.from_user.is_bot)
    client_id = user_id if user_id else message.from_user.id
    # if message.from_user.is_bot:  # Check if message is sent through bot's inline mode
    #     client_id = user_id
    # else:
    #     client_id = message.from_user.id
    basket = await get_user_basket(client_id)
    print(f' basket from payment process {basket}')
    basket_id = basket.basket_id

    amount = basket_total_value(basket_id)
    price = types.LabeledPrice(label='Your Order Total', amount=int(amount * 100))  # convert to cents
    await bot.send_invoice(message.chat.id,
                           title='Order Payment',
                           description='Paying for the products',
                           provider_token=PAY_TOKEN,
                           currency='uah',
                           photo_url=pic_link,
                           photo_height=316,
                           photo_width=316,
                           photo_size=316,
                           need_name=True,
                           need_phone_number=True,
                           need_email=True,
                           need_shipping_address=True,
                           send_phone_number_to_provider=True,
                           send_email_to_provider=True,
                           is_flexible=True,
                           prices=[price],
                           start_parameter='order-example',
                           payload='some-invoice-payload-for-our-internal-use',
                           reply_markup=None,

                           )

NP_SHIPPING = ShippingOption(id='np', title='NovaPoshta',
                             prices=[LabeledPrice(label='Nova Poshta Delivery', amount=5000)])
MEEST_SHIPPING = ShippingOption(id='mt', title='Meest',
                                prices=[LabeledPrice(label='Meest Delivery', amount=6000)])


async def shipping_check(shipping_query: ShippingQuery):
    """Provides shipping check"""

    shipping_options = []
    countries = ['UA']
    if shipping_query.shipping_address.country_code not in countries:
        return await bot.answer_shipping_query(shipping_query.id, ok=False,
                                               error_message="We can't deliver to your country")
    if shipping_query.shipping_address.country_code == 'UA':
        shipping_options.append(NP_SHIPPING)
        shipping_options.append(MEEST_SHIPPING)

    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options)


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def process_successful_payment(message: types.Message):
    """Processes successful payment"""

    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    # create a new order in the database
    await create_order(message)

    await bot.send_message(
        message.chat.id,
        f'Successful payment! '
        f'Amount: {message.successful_payment.total_amount // 100}{message.successful_payment.currency}'
        )
    await bot.send_message(
        message.chat.id,
        'Thank you for your order!\n'
        'Our manager will contact you soon.\n'
        'If you have any questions you can find our contact information on /start page'
    )


async def create_order(message: types.Message):
    """Creates an order using information entered by the user during the payment"""

    client_id = message.from_user.id
    basket = await get_user_basket(client_id)
    basket_id = basket.basket_id
    delivery_address = message.successful_payment.order_info.shipping_address.to_python()
    email = message.successful_payment.order_info.email
    phone = message.successful_payment.order_info.phone_number
    total_price = message.successful_payment.total_amount/100
    delivery_method = message.successful_payment.shipping_option_id
    session = SessionLocal()
    new_order = Order(
        client_id=client_id,
        # basket_id=basket_id,
        delivery_address=str(delivery_address),
        total_price=total_price,
        delivery_method=delivery_method,
        status='Received',
        items=basket.items,)
    session.add(new_order)
    client = session.query(Client).filter(Client.client_id == client_id).first()
    if client.email is None:
        client.email = email
    if client.phone is None:
        client.phone = phone
    if client.address is None:
        client.address = str(delivery_address)
    session.commit()
    session.close()
    await del_basket(basket)


async def del_basket(basket):
    """Deletes existing basket"""

    with SessionLocal() as session:
        session.delete(basket)
        session.commit()


