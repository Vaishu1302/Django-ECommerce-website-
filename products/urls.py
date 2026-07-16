from django.urls import path
from . import views


urlpatterns = [

    # --------------------
    # Product URLs
    # --------------------

    path(
        '',
        views.product_list,
        name='product_list'
    ),

    path(
        '<int:pk>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'add/',
        views.add_product,
        name='add_product'
    ),

    path(
        'edit/<int:pk>/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'delete/<int:pk>/',
        views.delete_product,
        name='delete_product'
    ),

    # --------------------
    # Category URLs
    # --------------------

    path(
        'categories/',
        views.category_list,
        name='category_list'
    ),

    path(
        'categories/add/',
        views.add_category,
        name='add_category'
    ),

    path(
        'categories/edit/<int:pk>/',
        views.edit_category,
        name='edit_category'
    ),

    path(
        'categories/delete/<int:pk>/',
        views.delete_category,
        name='delete_category'
    ),

]