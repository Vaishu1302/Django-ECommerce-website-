from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.cart_view,
        name='cart'
    ),

    path(
        'add/<int:pk>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'increase/<int:pk>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease/<int:pk>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    path(
        'remove/<int:pk>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

]