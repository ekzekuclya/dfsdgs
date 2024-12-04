import asyncio
from tempfile import NamedTemporaryFile
from aiogram import Router, Bot, F
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup, ChatMemberOwner, ChatMemberAdministrator, \
    KeyboardButton, CallbackQuery, InputFile, FSInputFile
from .start import start
from .text import menu_text, magazine_text, geo_text, payment_text, confirm_text, order_text, confirm_cancel, confirm_cancel_now, invoice_canceled
from django.db.models import Q, Count
from tg.models import TelegramUser, Geo, Product, Gram, Invoice
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from asgiref.sync import sync_to_async
from .apirone import create_invoice, check_invoice
import qrcode
router = Router()