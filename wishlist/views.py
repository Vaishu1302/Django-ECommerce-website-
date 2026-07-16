from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Wishlist
from products.models import Product
from cart.models import Cart
from django.core.paginator import Paginator

@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).order_by("-id")

    paginator = Paginator(
        wishlist_items,
        8          # Show 8 wishlist products per page
    )

    page_number = request.GET.get("page")

    wishlist_items = paginator.get_page(page_number)

    return render(
        request,
        "wishlist/wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    wishlist_item, created = Wishlist.objects.get_or_create(

        user=request.user,

        product=product

    )

    if created:

        messages.success(

            request,

            "Product added to wishlist."

        )

    else:

        messages.info(

            request,

            "Product is already in your wishlist."

        )

    return redirect("wishlist")


@login_required
def remove_from_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.filter(

        user=request.user,

        product=product

    ).delete()

    messages.success(

        request,

        "Product removed from wishlist."

    )

    return redirect("wishlist")


@login_required
def move_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart_item, created = Cart.objects.get_or_create(

        user=request.user,

        product=product,

        defaults={

            "quantity": 1

        }

    )

    if not created:

        cart_item.quantity += 1

        cart_item.save()

    Wishlist.objects.filter(

        user=request.user,

        product=product

    ).delete()

    messages.success(

        request,

        "Product moved to cart."

    )

    return redirect("cart")