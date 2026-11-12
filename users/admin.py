from django.contrib import admin
from .models import (
    UserProfile,
    FavoriteCurrency,
    RateAlert,
    UserActivity
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

@admin.register(FavoriteCurrency)
class RateAlertCurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'currency')
    search_fields = ('user__username', 'currency__code')

@admin.register(RateAlert)
class RateAlertAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'currency',
        'target_rate',
        'condition',
        'is_active'
    )
    list_filter = ('condition', 'is_active')

@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'action')