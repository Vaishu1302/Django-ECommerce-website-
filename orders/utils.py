from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(order):

    subject = f"Order Confirmation - Order #{order.id}"

    from_email = settings.DEFAULT_FROM_EMAIL

    recipient = [order.user.email]

    # Plain text fallback
    text_content = f"""
Hi {order.full_name},

Thank you for your order!

Your Order ID is {order.id}

Total Amount: ₹{order.total_amount}

Order Status: {order.status}

Thank you for shopping with us!
"""

    # HTML Email
    html_content = render_to_string(
        "emails/order_confirmation.html",
        {
            "order": order,
        },
    )

    email = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        recipient,
    )

    email.attach_alternative(
        html_content,
        "text/html",
    )

    email.send()