from django.contrib import admin
from .models import Product,Category
# Register your models here.
from django.contrib import admin
# from .models import Product, Category



# admin.site.register(Product)
# admin.site.register(Category)



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'category',
        'price',
        'stock',
    )

    list_filter = (
        'category',
    )

    search_fields = (
        'name',
    )