from django.contrib import admin


from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'product',
        'quantity',
        'added_at',
    )