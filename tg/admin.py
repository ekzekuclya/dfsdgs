from django.contrib import admin
from .models import TelegramUser, Geo, Product, Gram, Chapter, Invoice


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'balance', 'is_admin']


@admin.register(Geo)
class GeoAdmin(admin.ModelAdmin):
    list_display = ['geo_name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(Gram)
class GramAdmin(admin.ModelAdmin):
    list_display = ['id', 'gram']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['chapter_name', 'id']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id']