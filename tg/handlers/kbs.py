from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu = [
    [InlineKeyboardButton(text="🛒 Магазин", callback_data="start_buy")],
    [InlineKeyboardButton(text="🎁 Покупки", callback_data="user_history"),
     InlineKeyboardButton(text="🏷 Промокод", callback_data="add_promo")],
     [InlineKeyboardButton(text="👥 Рефералка", callback_data="ref"),
     InlineKeyboardButton(text="💬 Поддержка", callback_data="podd")],
    # [InlineKeyboardButton(text="⚠️ Правила", callback_data="rule"),
    # [InlineKeyboardButton(text="⚡️Наши ресурсы", callback_data="resources")],
    # [InlineKeyboardButton(text="☎️ Поддержка", url="https://t.me/Gazgolder_support1")],
    [InlineKeyboardButton(text="💱 Обменка #1", url="https://t.me/dino_obmenka")],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)


back_to_menu = [
    [InlineKeyboardButton(text="< Назад", callback_data="back_to_menu")]
]
back_to_menu = InlineKeyboardMarkup(inline_keyboard=back_to_menu)

menu_button = KeyboardButton(text="ℹ️ Показать меню")
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[menu_button]])

