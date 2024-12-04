import asyncio

from aiogram.client.session import aiohttp


async def get_balance(account_id, currency):
    url = f"https://apirone.com/api/v2/accounts/{account_id}/balance"
    params = {"currency": currency}

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


a = asyncio.run(get_balance("apr-295ca8ff52e454befc59a35c6e533333", "ltc"))
balance = a['balance']
print(balance)
amount = balance[0]['available']
print(amount)

