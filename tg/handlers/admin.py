from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject, BaseFilter
from aiogram.types import Message, InlineKeyboardButton, ReplyKeyboardMarkup, ChatMemberOwner, ChatMemberAdministrator, \
    KeyboardButton, CallbackQuery, KeyboardButton, ReplyKeyboardRemove
from .kbs import menu, menu_keyboard, admin
from .text import menu_text, order_text
from django.db.models import Q
from .start import start
from aiogram.fsm.context import FSMContext
from tg.models import TelegramUser, Invoice, Geo, Gram, Chapter, Product
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from asgiref.sync import sync_to_async
from aiogram.fsm.state import StatesGroup, State
router = Router()


@router.message(Command("admin"))
async def admin_panel(msg: Message):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=msg.from_user.id)
    if user.is_admin:
        await msg.answer("Привет Админ!", reply_markup=admin)


class AddProductState(StatesGroup):
    awaiting_geo = State()
    awaiting_gram = State()
    awaiting_chapter = State()
    awaiting_usd = State()
    adding_products = State()


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
        await state.set_state(AddProductState.awaiting_chapter)
    except Exception as e:
        print(e)


@router.message(AddProductState.awaiting_chapter)
async def awaiting_chapter(msg: Message, state: FSMContext):
    try:
        data = await state.get_data()
        geo_id = data.get("geo_id")
        gram_id = data.get("gram_id")
        geo = await sync_to_async(Geo.objects.get)(id=geo_id)
        gram = await sync_to_async(Gram.objects.get)(id=gram_id)
        chapter = await sync_to_async(Chapter.objects.get)(chapter_name=msg.text)
        await state.update_data(chapter_id=chapter.id)
        await msg.answer("Укажите цену в $", )
        await state.set_state(AddProductState.awaiting_usd)
    except Exception as e:
        print(e)


@router.message(AddProductState.awaiting_usd)
async def awaiting_ust(msg: Message, state: FSMContext):
    try:
        data = await state.get_data()
        geo_id = data.get("geo_id")
        gram_id = data.get("gram_id")
        chapter_id = data.get("chapter_id")
        geo = await sync_to_async(Geo.objects.get)(id=geo_id)
        gram = await sync_to_async(Gram.objects.get)(id=gram_id)
        chapter = await sync_to_async(Chapter.objects.get)(id=chapter_id)
        usd = msg.text
        usd = int(usd)
        await state.update_data(usd=usd)
        builder = ReplyKeyboardBuilder()
        builder.add(KeyboardButton(text="Завершить"))
        await msg.answer("Отправляйте продукты по 1", reply_markup=builder.as_markup())
        await state.set_state(AddProductState.adding_products)
    except Exception as e:
        print(e)


@router.message(AddProductState.adding_products)
async def add_products(msg: Message, state: FSMContext):
    if msg.text == "Завершить":
        await state.clear()
        await msg.answer("Завершено", reply_markup=ReplyKeyboardRemove())
        await start(msg)
    else:
        data = await state.get_data()
        geo_id = data.get("geo_id")
        gram_id = data.get("gram_id")
        chapter_id = data.get("chapter_id")
        usd = data.get("usd")
        geo = await sync_to_async(Geo.objects.get)(id=geo_id)
        gram = await sync_to_async(Gram.objects.get)(id=gram_id)
        chapter = await sync_to_async(Chapter.objects.get)(id=chapter_id)
        new_product = await sync_to_async(Product.objects.create)(geo=geo, gram=gram, chapter=chapter, price=usd,
                                                                  address=msg.text)
        await msg.answer(f"Продукт создан, {new_product.address}")
