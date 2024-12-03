from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup, ChatMemberOwner, ChatMemberAdministrator, \
    KeyboardButton, CallbackQuery
from .kbs import menu, menu_keyboard
from .text import menu_text, order_text
from django.db.models import Q
from tg.models import TelegramUser, Invoice
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from asgiref.sync import sync_to_async
from aiogram.fsm.state import StatesGroup, State
router = Router()


class ActiveInvoiceFilter(BaseFilter):
    async def __call__(self, msg: Message) -> bool:
        user_id = msg.from_user.id
        user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=user_id)
        if not user:
            return False
        has_active_invoice = await sync_to_async(Invoice.objects.filter)(user=user, active=True)
        has_active_invoice.exists()
        if has_active_invoice:
            return True


@router.message(ActiveInvoiceFilter())
async def active_invoice_handler(msg: Message, bot: Bot):
    user = await sync_to_async(TelegramUser.objects.get)(user_id=msg.from_user.id)
    invoice = await sync_to_async(Invoice.objects.filter)(user=user, active=True)
    invoice = invoice.first()
    if invoice is None:
        return
    text = order_text.format(order_id=invoice.id, req=invoice.req, ltc_sum=invoice.ltc_sum)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📱 Получить QR код для оплаты", callback_data=f"qr_{invoice.req}_{invoice.ltc_sum}"))
    builder.add(InlineKeyboardButton(text="🚫 Отменить", callback_data=f"conf_cancel_{invoice.id}"))
    builder.adjust(1)
    await msg.answer(text=text, parse_mode="Markdown", reply_markup=builder.as_markup())


class ActiveInvoiceCallbackFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery) -> bool:
        if callback.data.startswith("conf_cancel_"):
            return False
        if callback.data.startswith("cancel_"):
            return False
        if callback.data.startswith("back_to_order"):
            return False
        if callback.data.startswith("qr_"):
            return False
        if callback.data == "delete_qr":
            return False
        user_id = callback.from_user.id
        user = await sync_to_async(TelegramUser.objects.filter)(user_id=user_id)
        if not user.exists():
            return False
        has_active_invoice = await sync_to_async(Invoice.objects.filter)(user=user.first(), active=True)
        return has_active_invoice.exists()


@router.callback_query(ActiveInvoiceCallbackFilter())
async def block_buttons_handler(callback: CallbackQuery, bot: Bot):
    await callback.answer("Закончите пополнение по заявке или отмените её")


@router.message(F.text == "ℹ️ Показать меню")
@router.message(Command("start"))
async def start(msg: Message, bot: Bot, edit=None):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=msg.from_user.id)
    user.first_name = msg.from_user.first_name
    user.last_name = msg.from_user.last_name
    user.username = msg.from_user.username
    user.save()
    if created:
        text = "☀️ *Приветствие*"
        await msg.answer(text, reply_markup=menu_keyboard, parse_mode="Markdown")
    if edit:
        await msg.edit_text(menu_text, reply_markup=menu, parse_mode="Markdown")
    else:
        await msg.answer(menu_text, reply_markup=menu, parse_mode="Markdown")


@router.callback_query(F.data == "main_menu")
async def main_start(callback: CallbackQuery, edit=None):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=callback.message.from_user.id)
    user.first_name = callback.message.from_user.first_name
    user.last_name = callback.message.from_user.last_name
    user.username = callback.message.from_user.username
    user.save()
    await callback.message.edit_text(menu_text, reply_markup=menu, parse_mode="Markdown")
