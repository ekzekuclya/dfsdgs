import asyncio

from aiogram.client.session import aiohttp


async def main(satoshis):
    amount1 = int(satoshis * 0.13)  # 13% от суммы (уже в сатоши)
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


