from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup, ChatMemberOwner, ChatMemberAdministrator, \
    KeyboardButton, CallbackQuery
from .kbs import menu, menu_keyboard
from .text import menu_text, order_text, ref_text
from django.db.models import Q
from tg.models import TelegramUser, Invoice
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from asgiref.sync import sync_to_async
from aiogram.fsm.state import StatesGroup, State
router = Router()


@router.callback_query(F.data == "ref")
async def refs(callback: CallbackQuery, bot: Bot):
    bot_user = await bot.get_me()
    text = ref_text.format(bot=bot_user.username)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="‹ Назад", callback_data="back_to_menu"))
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
