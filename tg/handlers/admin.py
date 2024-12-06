from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup, ChatMemberOwner, ChatMemberAdministrator, \
    KeyboardButton, CallbackQuery, KeyboardButton
from .kbs import menu, menu_keyboard
from .text import menu_text, order_text
from django.db.models import Q
from aiogram.fsm.context import FSMContext
from tg.models import TelegramUser, Invoice, Geo, Gram, Chapter
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from asgiref.sync import sync_to_async
from aiogram.fsm.state import StatesGroup, State
router = Router()


class AddProductState(StatesGroup):
    awaiting_geo = State()
    awaiting_gram = State()
    awaiting_chapter = State()


@router.callback_query(F.data == "add_products")
async def add_products(callback: CallbackQuery, state: FSMContext):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=callback.from_user.id)
    if user.is_admin:
        geos = await sync_to_async(Geo.objects.all)()
        builder = ReplyKeyboardBuilder()
        for i in geos:
            builder.add(KeyboardButton(text=f"{i.geo_name}"))
        await state.set_state(AddProductState.awaiting_geo)
        await callback.message.answer("Выберите район", reply_markup=builder.as_markup())


@router.message(AddProductState.awaiting_geo)
async def awaiting_geo(msg: Message, state: FSMContext):
    try:
        geo = await sync_to_async(Geo.objects.get)(geo_name=msg.text)
        grams = await sync_to_async(Gram.objects.all)()
        builder = ReplyKeyboardBuilder()
        for i in grams:
            builder.add(KeyboardButton(text=f"{i.gram}"))
        await msg.answer("Выберите грамовку", reply_markup=builder.as_markup())
        await state.update_data(geo_id=geo.id)
        await state.set_state(AddProductState.awaiting_gram)
    except Exception as e:
        print(e)


@router.message(AddProductState.awaiting_gram)
async def awaiting_gram(msg: Message, state: FSMContext):
    try:
        data = await state.get_data()
        geo_id = data.get("geo_id")
        geo = await sync_to_async(Geo.objects.get)(id=geo_id)
        gram = await sync_to_async(Gram.objects.get)(gram=msg.text)
        chapters = await sync_to_async(Chapter.objects.all)()
        builder = ReplyKeyboardBuilder()
        for i in chapters:
            builder.add(KeyboardButton(text=f"{i.chapter_name}"))
        await state.update_data(gram_id=gram.id)
        await msg.answer("Какой продукт хотите добавить?", reply_markup=builder.as_markup())
    except Exception as e:
        print(e)