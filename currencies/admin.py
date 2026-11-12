from django.contrib import admin
from .models import (
    CurrencyCategory,
    Currency,
    RateSource,
    ExchangeRate,
    ImportLog
)


@admin.register(CurrencyCategory)
class CurrencyCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'symbol', 'category')
    list_filter = ('category',)
    search_fields = ('code', 'name')


@admin.register(RateSource)
class RateSourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'api_url', 'is_active')
    list_filter = ('is_active',)


@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'currency',
        'base_currency',
        'rate',
        'date',
        'source'
    )
    list_filter = ('date', 'source')
    search_fields = ('currency__code', 'base_currency__code')


@admin.register(ImportLog)
class ImportLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'import_date', 'status')
    list_filter = ('status', 'import_date')