from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from orders.models import Order
from .models import Payment
from .utils import create_razorpay_order, verify_payment_signature


@login_required
def payment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    # Create Razorpay Order
    razorpay_order = create_razorpay_order(
        order.total_amount
    )

    # Save Payment Details
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            "amount": order.total_amount,
            "razorpay_order_id": razorpay_order["id"],
        }
    )

    if not created:
        payment.razorpay_order_id = razorpay_order["id"]
        payment.save()

    context = {

        "order": order,

        "payment": payment,

        "razorpay_order_id": razorpay_order["id"],

        "razorpay_key": "YOUR_RAZORPAY_KEY_ID",

        "amount": int(order.total_amount * 100),

    }

    return render(
        request,
        "payments/payment.html",
        context
    )


@login_required
def verify(request):

    if request.method == "POST":

        razorpay_order_id = request.POST.get(
            "razorpay_order_id"
        )

        razorpay_payment_id = request.POST.get(
            "razorpay_payment_id"
        )

        razorpay_signature = request.POST.get(
            "razorpay_signature"
        )

        payment = get_object_or_404(
            Payment,
            razorpay_order_id=razorpay_order_id
        )

        verified = verify_payment_signature(

            razorpay_order_id,

            razorpay_payment_id,

            razorpay_signature,

        )

        if verified:

            payment.razorpay_payment_id = razorpay_payment_id

            payment.razorpay_signature = razorpay_signature

            payment.status = "Success"

            payment.save()

            order = payment.order

            order.payment_status = "Paid"

            order.status = "Processing"

            order.save()

            return redirect(
                "payment_success",
                order.id
            )

        else:

            payment.status = "Failed"

            payment.save()

            return redirect(
                "payment_failed",
                payment.order.id
            )

    return redirect("home")


@login_required
def payment_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "payments/payment_success.html",
        {
            "order": order
        }
    )


@login_required
def payment_failed(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "payments/payment_failed.html",
        {
            "order": order
        }
    )