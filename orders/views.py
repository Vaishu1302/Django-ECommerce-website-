from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from .forms import CheckoutForm
from .utils import send_order_confirmation_email
from django.core.paginator import Paginator
@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("cart")

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        form = CheckoutForm(request.POST)

        if form.is_valid():

            order = form.save(commit=False)

            order.user = request.user

            order.total_amount = total

            order.payment_status = "Pending"

            order.status = "Pending"

            order.save()

            for item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

        # Send Order Confirmation Email
        if order.user.email:
            send_order_confirmation_email(order)

        # Clear Cart
        cart_items.delete()

        return redirect("order_success", order.id)

    else:

        form = CheckoutForm()

    return render(
        request,
        "orders/checkout.html",
        {
            "form": form,
            "cart_items": cart_items,
            "total": total,
        },
    )
from django.core.paginator import Paginator

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    paginator = Paginator(orders, 5)   # Show 5 orders per page

    page_number = request.GET.get("page")

    orders = paginator.get_page(page_number)

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_detail.html",
        {
            "order": order
        }
    )
@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    # Allow cancellation only before shipping
    if order.status in ["Pending", "Confirmed", "Processing"]:

        order.status = "Cancelled"
        order.save()

        # Restore product stock
        for item in order.items.all():

            product = item.product
            product.stock += item.quantity
            product.save()

        messages.success(
            request,
            "Your order has been cancelled successfully."
        )

    else:

        messages.error(
            request,
            "This order cannot be cancelled."
        )

    return redirect("order_detail", order_id=order.id)
@login_required
def order_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "orders/order_success.html",
        {
            "order": order
        }
    )