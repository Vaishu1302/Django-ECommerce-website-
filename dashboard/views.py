from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from orders.models import Order
from wishlist.models import Wishlist
from cart.models import Cart


@login_required
def dashboard(request):

    total_orders = Order.objects.filter(
        user=request.user
    ).count()

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    cart_count = Cart.objects.filter(
        user=request.user
    ).count()

    total_spent = sum(

        order.total_amount

        for order in Order.objects.filter(
            user=request.user
        )

    )

    latest_order = Order.objects.filter(
        user=request.user
    ).order_by("-created_at").first()

    context = {

        "total_orders": total_orders,

        "wishlist_count": wishlist_count,

        "cart_count": cart_count,

        "total_spent": total_spent,

        "latest_order": latest_order,

    }

    return render(
        request,
        "dashboard/dashboard.html",
        context,
    )