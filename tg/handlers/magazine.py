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


@router.callback_query(F.data == "start_buy")
async def magazine(callback: CallbackQuery, bot: Bot):
    geo_with_products = await sync_to_async(Geo.objects.filter)(product__isnull=False, product__byed_by__isnull=True, product__reserved=False)
    geo_with_products = geo_with_products.distinct()

    builder = InlineKeyboardBuilder()
    for geo in geo_with_products:
        builder.add(InlineKeyboardButton(text=f"{geo.geo_name}", callback_data=f"geo_{geo.id}"))
    builder.add(InlineKeyboardButton(text="‹ Назад", callback_data="back_to_menu"))
    builder.adjust(1)
    await callback.message.edit_text(magazine_text, reply_markup=builder.as_markup(), parse_mode="Markdown")


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, bot: Bot):
    await start(callback.message, bot, True)


@router.callback_query(F.data.startswith("geo_"))
async def choose_gram(callback: CallbackQuery, bot: Bot):
    geo_id = callback.data.split("_")[1]
    geo = await sync_to_async(Geo.objects.get)(id=geo_id)
    products = await sync_to_async(Product.objects.filter)(geo_name=geo, byed_by__isnull=True, reserved=False)
    gram_set = products.values_list('gram__gram', flat=True)
    gram_set = gram_set.distinct()

    builder = InlineKeyboardBuilder()
    for gram in gram_set:
        products_for_gram = products.filter(gram__gram=gram)
        if products_for_gram.exists():
            product = products_for_gram.first()
            button_text = f"{product.product_name.chapter_name} - {gram}г - {product.price}$"
            builder.add(InlineKeyboardButton(text=button_text, callback_data=f"gram_{geo.id}_{gram}_{product.id}"))

    builder.add(InlineKeyboardButton(text="‹ Назад", callback_data=f"start_buy"))
    builder.adjust(1)
    await callback.message.edit_text(geo_text, reply_markup=builder.as_markup(), parse_mode="Markdown")


@router.callback_query(F.data.startswith("gram_"))
async def choose_payment(callback: CallbackQuery, bot: Bot):
    data = callback.data.split("_")
    geo_id = data[1]
    gram = data[2]
    product_id = data[3]
    geo = await sync_to_async(Geo.objects.get)(id=geo_id)
    gram = await sync_to_async(Gram.objects.get)(gram=gram)
    product = await sync_to_async(Product.objects.get)(id=product_id)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="LiteCoin", callback_data=f"ltc_{geo.id}_{gram.id}_{product.id}"))
    builder.add(InlineKeyboardButton(text="‹ Назад", callback_data=f"geo_{geo.id}"))
    builder.adjust(1)
    text = payment_text.format(geo=geo.geo_name, product=product.product_name.chapter_name)
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")


@router.callback_query(F.data.startswith("ltc_"))
async def ltc_payment(callback: CallbackQuery, bot: Bot):
    data = callback.data.split("_")
    geo_id = data[1]
    gram_id = data[2]
    product_id = data[3]
    geo = await sync_to_async(Geo.objects.get)(id=geo_id)
    gram = await sync_to_async(Gram.objects.get)(id=gram_id)
    product = await sync_to_async(Product.objects.get)(id=product_id)
    text = confirm_text.format(geo=geo.geo_name, product=product.product_name.chapter_name, gram=gram.gram, price=product.price)

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Подтвердить", callback_data=f"confirm_{geo.id}_{gram.id}_{product.id}"))
    builder.add(InlineKeyboardButton(text="‹ Назад", callback_data=f"gram_{geo.id}_{gram}_{product.id}"))
    builder.adjust(1)
    await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")


# invoice = a['invoice']
# amount_in_satoshi = a['amount']
# address = a['address']
# amount_in_ltc = amount_in_satoshi / 10 ** 8
# asyncio.create_task(check_invoice_paid(invoice, callback_query.message, product, product.gram.chapter, user))

@router.callback_query(F.data.startswith("confirm_"))
async def confirm(callback: CallbackQuery, bot: Bot):
    data = callback.data.split("_")
    print(data)
    geo_id = data[1]
    gram_id = data[2]
    product_id = data[3]
    geo = await sync_to_async(Geo.objects.get)(id=geo_id)
    gram = await sync_to_async(Gram.objects.get)(id=gram_id)
    product = await sync_to_async(Product.objects.get)(id=product_id)
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=callback.from_user.id)
    invoice = await sync_to_async(Invoice.objects.filter)(user=user, active=True)
    order = await create_invoice(product, "ltc")
    if not invoice and order:
        invoice_id = order["invoice"]
        amount_satoshi = order["amount"]
        req = order["address"]
        amount_ltc = amount_satoshi / 10 ** 8
        invoice = await sync_to_async(Invoice.objects.create)(user=user, req=req, ltc_sum=amount_ltc)
        text = order_text.format(order_id=invoice.id, req=req, ltc_sum=amount_ltc)
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="📱 Получить QR код для оплаты", callback_data=f"qr_{req}_{amount_ltc}"))
        builder.add(InlineKeyboardButton(text="🚫 Отменить", callback_data=f"conf_cancel_{invoice.id}"))
        builder.adjust(1)
        await callback.message.edit_text(text, reply_markup=builder.as_markup(), parse_mode="Markdown")
        products = await sync_to_async(Product.objects.filter)(geo_name=product.geo_name, gram=product.gram,
                                                               byed_by__isnull=True, reserved=False)

        random_product = await sync_to_async(products.order_by('?').first)()
        random_product.reserved = True
        random_product.save()
        invoice.reserved_product = random_product
        invoice.save()
        asyncio.create_task(check_invoice(invoice_id, callback.message, random_product, user, invoice))


@router.callback_query(F.data.startswith("conf_cancel_"))
async def confirm_cancel(callback: CallbackQuery):
    data = callback.data.split("_")
    inv_id = data[2]
    invoice = await sync_to_async(Invoice.objects.get)(id=inv_id)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Да", callback_data=f"cancel_{invoice.id}"))
    builder.add(InlineKeyboardButton(text="Нет", callback_data=f"back_to_order"))
    builder.adjust(2)
    await callback.message.edit_text(confirm_cancel_now, reply_markup=builder.as_markup(), parse_mode="Markdown")


@router.callback_query(F.data == "back_to_order")
async def back_to_order(callback: CallbackQuery):
    user = await sync_to_async(TelegramUser.objects.get)(user_id=callback.from_user.id)
    invoice = await sync_to_async(Invoice.objects.filter)(user=user, active=True)
    print(invoice)
    invoice = invoice.first()
    if not invoice:
        print("INVOICE IS NONE")
        return
    text = order_text.format(order_id=invoice.id, req=invoice.req, ltc_sum=invoice.ltc_sum)
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📱 Получить QR код для оплаты", callback_data=f"qr_{invoice.req}_{invoice.ltc_sum}"))
    builder.add(InlineKeyboardButton(text="🚫 Отменить", callback_data=f"conf_cancel_{invoice.id}"))
    builder.adjust(1)
    await callback.message.edit_text(text=text, parse_mode="Markdown", reply_markup=builder.as_markup())


@router.callback_query(F.data.startswith("cancel_"))
async def cancel_invoice(callback: CallbackQuery):
    invoice_id = callback.data.split("_")[1]
    invoice = await sync_to_async(Invoice.objects.get)(id=invoice_id)
    invoice.active = False
    invoice.save()
    if invoice.reserved_product:
        invoice.reserved_product.reserved = False
        invoice.reserved_product.save()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="‹ На главную", callback_data="main_menu"))
    await callback.message.edit_text(invoice_canceled, reply_markup=builder.as_markup(), parse_mode="Markdown")
    return


@router.callback_query(F.data.startswith("qr_"))
async def show_qr(callback: CallbackQuery, bot: Bot):
    data = callback.data.split("_")
    req = data[1]
    amount = data[2]
    ltc_data = f"litecoin:{req}?amount={amount}"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=1,
    )
    qr.add_data(ltc_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        img.save(temp_file, format="PNG")
        temp_file_path = temp_file.name
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="❌ Закрыть", callback_data="delete_qr"))
    await bot.send_photo(
        chat_id=callback.message.chat.id,
        photo=FSInputFile(temp_file_path), reply_markup=builder.as_markup())


@router.callback_query(F.data == "delete_qr")
async def delete_qr(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()


