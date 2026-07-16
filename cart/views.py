from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import Cart
from products.models import Product


@login_required
def cart_view(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:

        item.subtotal = item.product.price * item.quantity

        total += item.subtotal

    return render(
        request,
        "cart/cart.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )


@login_required
def add_to_cart(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


@login_required
def increase_quantity(request, pk):

    cart = get_object_or_404(
        Cart,
        id=pk,
        user=request.user
    )

    cart.quantity += 1
    cart.save()

    return redirect("cart")


@login_required
def decrease_quantity(request, pk):

    cart = get_object_or_404(
        Cart,
        id=pk,
        user=request.user
    )

    if cart.quantity > 1:
        cart.quantity -= 1
        cart.save()
    else:
        cart.delete()

    return redirect("cart")


@login_required
def remove_from_cart(request, pk):

    cart = get_object_or_404(
        Cart,
        id=pk,
        user=request.user
    )

    cart.delete()

    return redirect("cart")