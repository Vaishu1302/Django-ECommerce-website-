from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):

    PAYMENT_CHOICES = [

        ("Cash on Delivery", "Cash on Delivery"),

    ]

    PAYMENT_STATUS = [

        ("Pending", "Pending"),

        ("Paid", "Paid"),

    ]

    STATUS_CHOICES = [

        ("Pending", "Pending"),

        ("Confirmed", "Confirmed"),

        ("Processing", "Processing"),

        ("Shipped", "Shipped"),

        ("Delivered", "Delivered"),

        ("Cancelled", "Cancelled"),

    ]

    user = models.ForeignKey(

        User,

        on_delete=models.CASCADE

    )

    full_name = models.CharField(

        max_length=100

    )

    phone = models.CharField(

        max_length=15

    )

    address = models.TextField()

    city = models.CharField(

        max_length=100

    )

    state = models.CharField(

        max_length=100

    )

    pincode = models.CharField(

        max_length=10

    )
    country = models.CharField(
    max_length=100,
    default="India"
)

    total_amount = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    payment_method = models.CharField(

        max_length=30,

        choices=PAYMENT_CHOICES,

        default="Cash on Delivery"

    )

    payment_status = models.CharField(

        max_length=20,

        choices=PAYMENT_STATUS,

        default="Pending"

    )

    status = models.CharField(

        max_length=20,

        choices=STATUS_CHOICES,

        default="Pending"

    )

    created_at = models.DateTimeField(

        auto_now_add=True

    )

    def __str__(self):

        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):

    order = models.ForeignKey(

        Order,

        on_delete=models.CASCADE,

        related_name="items"

    )

    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE

    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )

    def subtotal(self):

        return self.quantity * self.price

    def __str__(self):

        return self.product.name