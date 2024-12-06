from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup, ChatMemberOwner, ChatMemberAdministrator, \
    KeyboardButton, CallbackQuery
from .kbs import menu, menu_keyboard
from .text import menu_text, order_text, pokupka_text
from django.db.models import Q
from tg.models import TelegramUser, Invoice, Product
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from asgiref.sync import sync_to_async
from aiogram.fsm.state import StatesGroup, State
router = Router()


@router.callback_query(F.data=="user_history")
async def user_history(callback: CallbackQuery):
    text = "🎁 *Покупки*\n\nНиже представлен список Ваших покупок в магазине:"
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=callback.from_user.id)
    user_products = await sync_to_async(Product.objects.filter)(byed_by=user)
    builder = InlineKeyboardBuilder()
    if user_products:
        for i in user_products:
            builder.add(InlineKeyboardButton(text=f"{i.product_name.chapter_name} от {i.date_add}", callback_data=f"show_user_{i.id}"))
    else:
        builder.add(InlineKeyboardButton(text="Покупки отсутствуют", callback_data="asd"))
    builder.add(InlineKeyboardButton(text="‹ Назад", callback_data="back_to_menu"))
    builder.adjust(1)
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")


@router.callback_query(F.data.startswith("show_user_"))
async def show_user_history(callback: CallbackQuery):
    product_id = callback.data.split("_")[2]
    product = await sync_to_async(Product.objects.get)(id=product_id)
    text = pokupka_text.format(num=product.id, geo=product.geo.geo_name,
                               product_name=product.product_name.chapter_name, adr=product.address)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="‹ Назад", callback_data="user_history"))
    await callback.message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
