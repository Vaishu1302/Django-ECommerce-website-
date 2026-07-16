from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order


@receiver(pre_save, sender=Order)
def send_order_status_email(sender, instance, **kwargs):

    # New order, don't send status update email
    if not instance.pk:
        return

    try:
        old_order = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return

    # Only send email if status changed
    if old_order.status != instance.status:

        subject = f"Order #{instance.id} Status Updated"

        from_email = settings.DEFAULT_FROM_EMAIL

        recipient = [instance.user.email]

        # Plain text version
        text_content = f"""
Hello {instance.full_name},

Your order status has changed.

Order ID: {instance.id}

New Status: {instance.status}

Payment Status: {instance.payment_status}

Thank you for shopping with us!

E-Commerce Team
"""

        # HTML version
        html_content = render_to_string(
            "emails/order_status_update.html",
            {
                "order": instance,
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