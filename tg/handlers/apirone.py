from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import ClientConnectorError
from django.db.models import Q
from tg.models import Product
from asgiref.sync import sync_to_async
import aiohttp
import asyncio
from aiogram import exceptions as tg_exceptions
import requests


async def create_invoice(product, crypto):
    account = "apr-295ca8ff52e454befc59a35c6e533333"
    create_invoice_url = f'https://apirone.com/api/v2/accounts/{account}/invoices'
    course = await get_crypto_with_retry(crypto)
    if course is not None:
        ltc_price = product.price / course

        decimal_places = 8

        amount_in_satoshi = int(ltc_price * 10 ** decimal_places)
        invoice_data = {
            "amount": amount_in_satoshi,
            "currency": "ltc",
            "lifetime": 2000,
            "callback_url": "http://example.com",
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(create_invoice_url, json=invoice_data, headers={'Content-Type': 'application/json'}
                                        ) as response:
                    invoice_info = await response.json()

            return invoice_info
        except ClientConnectorError as e:
            await create_invoice(product, crypto)


async def get_crypto_with_retry(crypto, max_retries=10):
    url = f"https://apirone.com/api/v2/ticker?currency={crypto}"

    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    json_data = await response.json()

            return json_data.get('usd')
        except aiohttp.ClientConnectorError as e:
            print(f"Ошибка при получении курса криптовалюты. Попытка {attempt + 1}/{max_retries}")
            await asyncio.sleep(1)

    print("Не удалось получить курс криптовалюты после нескольких попыток.")
    return None


async def check_invoice(invoice_id, msg, product, user, order):
    while True:
        url = f"https://apirone.com/api/v2/invoices/{invoice_id}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        invoice_data = await response.json()
                        if invoice_data['status'] == 'partpaid':
                            for i in invoice_data['history']:
                                if i['status'] == 'partpaid':
                                    course = await get_crypto_with_retry('ltc')
                                    amount = float(i['amount']) / 10 ** 8
                                    usd_amount = amount * course
                                    usd_amount = int(usd_amount)
                                    product.reserved = False
                                    product.save()
                                    if usd_amount >= 1:
                                        user.balance += int(usd_amount)
                                        user.save()
                                        order.active = False
                                        order.save()
                                        break
                        if invoice_data['status'] == 'completed':
                            await msg.answer(f"{product.address}")
                            product.byed_by = user
                            product.save()
                            order.active = False
                            order.save()
                            print(invoice_data['amount'])
                            total_amount = float(invoice_data['amount'])
                            asyncio.create_task(waiting_balance(total_amount))
                            break
                        if invoice_data['status'] == 'expired':
                            order.active = False
                            order.save()
                            product.reserved = False
                            product.save()
                            break
                        await asyncio.sleep(10)
                    else:
                        print(f"Connection error:")
                        print("Retrying in 5 seconds...")
                        await asyncio.sleep(5)

        except ClientConnectorError as e:
            print(f"Connection error: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)
        except tg_exceptions.TelegramNetworkError as e:
            print(f"Telegram Network error: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)


async def waiting_balance(total_amount):
    count = 0
    while True:
        balance_data = await get_balance("apr-295ca8ff52e454befc59a35c6e533333")
        balance = balance_data['balance']
        amount = balance[0]['available']
        if balance_data and amount >= total_amount:
            await transfer(total_amount)
        else:
            print("Insufficient funds or balance data is unavailable.")
        count += 1
        await asyncio.sleep(10)
        if count == 10:
            break


async def transfer(satoshis):
    amount1 = int(satoshis * 0.12)  # 13% от суммы (уже в сатоши)
    amount2 = satoshis - amount1  # Остаток
    transfer_key = "0PzLuwx5OlQ4HPThMqbEO1NUKiBKntBl"
    url = f"https://apirone.com/api/v2/accounts/apr-295ca8ff52e454befc59a35c6e533333/transfer"
    print("AMOUNT 1:", amount1)
    print("AMOUNT 2:", amount2)
    headers = {'Content-Type': 'application/json'}
    payload = {
        "currency": "ltc",
        "transfer-key": transfer_key,
        "destinations": [
            {
                "address": "LWbyjqd5sS7YLMiNha7aArabs2mLtQd8Cg",
                "amount": amount1
            },
            {
                "address": "LYkX62hDtWGxRV47Wxn5j7HBmUT5cKUTAW",
                "amount": amount2}
        ],
        "fee": "normal",
        "subtract-fee-from-amount": True
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                print("Transfer successful:", result)
            else:
                print(f"Failed transfer. Status code: {response.status}")
                error_message = await response.text()
                print("Error message:", error_message)


async def get_balance(account_id):
    url = f"https://apirone.com/api/v2/accounts/{account_id}/balance"
    params = {"currency": "ltc"}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    balance_data = await response.json()
                    return balance_data
                else:
                    print(f"Failed to fetch balance. Status: {response.status}")
                    error_message = await response.text()
                    print(f"Error message: {error_message}")
                    return None
    except Exception as e:
        print(f"Error fetching balance: {e}")
        return None
