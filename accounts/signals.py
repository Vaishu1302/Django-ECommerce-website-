from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import UserProfile


@receiver(post_save, sender=User)

def create_profile(sender, instance, created, **kwargs):

    if created:

        UserProfile.objects.create(
            user=instance
        )


@receiver(post_save, sender=User)

def save_profile(sender, instance, **kwargs):

    instance.userprofile.save()
@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):

    if created:

        subject = "Welcome to Our E-Commerce Store"

        message = f"""
Hi {instance.first_name or instance.username},

Welcome to our E-Commerce Website!

Thank you for creating your account.

You can now:

• Browse products
• Add items to your cart
• Place orders
• Track your orders
• Manage your wishlist

Happy Shopping!

Regards,
E-Commerce Team
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [instance.email],
            fail_silently=False,
        )