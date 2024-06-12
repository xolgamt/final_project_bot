from typing import List
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from models import Basket, Order
from utils.database import SessionLocal, get_user_basket, basket_total_value


async def process_order_client(call: CallbackQuery, state: FSMContext):
    client_id = call.from_user.id
    print(f"client_id: {client_id}")
    basket = await get_user_basket(client_id)
    if not basket:
        await call.answer(text="Your basket is empty")
        return
    basket_id = basket.basket_id
    # basket_id = call.from_user.id
    session = SessionLocal()

    # Get the total price of the order
    total_price = basket_total_value(basket_id)
    # Create the order
    order = Order(
        client_id=client_id,
        basket_id=basket_id,
        total_price=total_price,
        delivery_method='None',
        delivery_address='None',
        status="created",
        items=basket.items
    )
    session.add(order)
    session.commit()

    # # create an order from the basket
    # order = Order(
    #     client_id=basket.client_id,
    #     basket_id=basket.basket_id,
    #     items=basket.items,
    #     total_price=sum(basket.items.values()),
    #     delivery_method='standard',
    #     delivery_address='123 Main St.',
    #     status='pending'
    # )
    #
    # try:
    #     session.add(order)
    #     session.delete(basket)
    #     session.commit()
    # except IntegrityError:
    #     session.rollback()
    #     print('Error: Only one order can be created from each basket.')
    #


    # Save the items of the basket as the order's items
    # order_items = []
    # for item in basket.items:
    #     product = item[1]
    #     order_items.append(
    #         {
    #             "product_id": product.product_id,
    #             "quantity": item['quantity'],
    #             "price": product.price,
    #         }
    #     )
    # order.items = order_items
    session.add(order)
    session.commit()
    # Delete the basket
    session.delete(basket)
    session.commit()
    # Send the invoice
    await call.answer()
    await call.message.answer_invoice(
        title="Your Order",
        description="",
        payload=f"order:{order.order_id}",
        provider_token="<YOUR_PROVIDER_TOKEN>",
        start_parameter="order",
        currency="UAH",
        prices=[
            types.LabeledPrice(
                label="Order total",
                amount=int(total_price * 100),
            )
        ],
        need_shipping_address=True,
        is_flexible=True,
    )

    # Save the order ID in the state for later use
    await state.update_data(order_id=order.order_id)

# class CheckoutForm(StatesGroup):
#     name = State()
#     email = State()
#     phone = State()
#     address = State()
#
# @dp.callback_query_handler(text="process_order")
# async def handle_process_order(call: CallbackQuery, state: FSMContext):
#     await process_order(call, state)
#
# @dp.shipping_query_handler()
# async def process_shipping_query(query: types.ShippingQuery):
#     await bot.answer_shipping_query(
#         query.id,
#         ok=True,
#         shipping_options=[
#             types.ShippingOption(
#                 id="standard",
#                 title="Standard Shipping",
#                 prices=[
#                     types.LabeledPrice(label="Shipping", amount=1000),
#                 ],
#             ),
#             types.ShippingOption(
#                 id="express",
#                 title="Express Shipping",
#                 prices=[
#                     types.LabeledPrice(label="Shipping", amount=2000),
#                 ],
#             ),
#         ],
#     )
#
# state: FSMContext):
# await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
# await bot.send_message(pre_checkout_query.from_user.id, "Please fill out the checkout form:")
# await CheckoutForm.name.set()
#
# @dp.message_handler(Command("checkout"), state="*")
# async def cmd_start(message: types.Message, state: FSMContext):
# await message.answer("Please enter your name:")
# await CheckoutForm.name.set()
#
# @dp.message_handler(state=CheckoutForm.name)
# async def process_name(message: types.Message, state: FSMContext):
# async with state.proxy() as data:
# data["name"] = message.text
# await message.answer("Please enter your email address:")
# await CheckoutForm.email.set()
#
# @dp.message_handler(state=CheckoutForm.email)
# async def process_email(message: types.Message, state: FSMContext):
# async with state.proxy() as data:
# data["email"] = message.text
# await message.answer("Please enter your phone number:")
# await CheckoutForm.phone.set()
#
# @dp.message_handler(state=CheckoutForm.phone)
# async def process_phone(message: types.Message, state: FSMContext):
# async with state.proxy() as data:
# data["phone"] = message.text
# await message.answer("Please enter your address:")
# await CheckoutForm.address.set()
#
# @dp.message_handler(state=CheckoutForm.address)
# async def process_address(message: types.Message, state: FSMContext):
# async with state.proxy() as data:
# data["address"] = message.text
# await message.answer("Thank you! Please wait while we process your order.")
#
#
# # Retrieve order information from state
# async with state.proxy() as data:
#     order_info = {
#         "name": data["name"],
#         "email": data["email"],
#         "phone": data["phone"],
#         "address": data["address"],
#     }
#
# # Send the order to be processed
# await process_order(order_info)
#
# # Clear state
# await state.finish()
#


