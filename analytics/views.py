from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import (
    Sum,
    Count,
    Avg,
    F,
    DecimalField,
    ExpressionWrapper,
)

from django.db.models.functions import TruncMonth

from django.utils import timezone
from datetime import timedelta

import json

from orders.models import Order, OrderItem
from products.models import Product
from django.contrib.auth.decorators import user_passes_test
def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)

@login_required
def dashboard(request):

    # -----------------------------
    # Dashboard Summary
    # -----------------------------

    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_customers = User.objects.count()

    total_revenue = (
        Order.objects.filter(payment_status="Paid")
        .aggregate(total=Sum("total_amount"))["total"] or 0
    )

    # -----------------------------
    # Order Status Counts
    # -----------------------------

    pending_orders = Order.objects.filter(status="Pending").count()
    processing_orders = Order.objects.filter(status="Processing").count()
    shipped_orders = Order.objects.filter(status="Shipped").count()
    delivered_orders = Order.objects.filter(status="Delivered").count()
    cancelled_orders = Order.objects.filter(status="Cancelled").count()

    # -----------------------------
    # Payment Status Counts
    # -----------------------------

    paid_orders = Order.objects.filter(payment_status="Paid").count()
    pending_payments = Order.objects.filter(payment_status="Pending").count()
    failed_payments = Order.objects.filter(payment_status="Failed").count()

    # -----------------------------
    # Low Stock Products
    # -----------------------------

    low_stock_products = Product.objects.filter(stock__lte=5)

    # -----------------------------
    # Monthly Sales
    # -----------------------------

    monthly_sales = (
        Order.objects.filter(payment_status="Paid")
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("total_amount"))
        .order_by("month")
    )

    months = []
    sales = []

    for item in monthly_sales:
        months.append(item["month"].strftime("%b %Y"))
        sales.append(float(item["total"]))

    # -----------------------------
    # Best Selling Products
    # -----------------------------

    best_selling_products = (
        OrderItem.objects
        .values("product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )

    # -----------------------------
    # Top Customers
    # -----------------------------

    top_customers = (
        Order.objects.filter(payment_status="Paid")
        .values(
            "user__username",
            "user__first_name",
            "user__last_name",
        )
        .annotate(
            total_spent=Sum("total_amount"),
            total_orders=Count("id"),
        )
        .order_by("-total_spent")[:5]
    )

    # -----------------------------
    # Revenue by Category
    # -----------------------------

    category_sales = (
        OrderItem.objects
        .annotate(
            revenue=ExpressionWrapper(
                F("price") * F("quantity"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
        .values("product__category__name")
        .annotate(revenue=Sum("revenue"))
        .order_by("-revenue")
    )

    category_names = []
    category_revenue = []

    for item in category_sales:
        category_names.append(item["product__category__name"])
        category_revenue.append(float(item["revenue"]))

    # -----------------------------
    # Recent Orders
    # -----------------------------

    recent_orders = (
        Order.objects
        .select_related("user")
        .order_by("-created_at")[:10]
    )

    # -----------------------------
    # Top Categories
    # -----------------------------

    top_categories = (
        OrderItem.objects
        .annotate(
            revenue=ExpressionWrapper(
                F("price") * F("quantity"),
                output_field=DecimalField(max_digits=12, decimal_places=2),
            )
        )
        .values("product__category__name")
        .annotate(
            total_products_sold=Sum("quantity"),
            total_revenue=Sum("revenue"),
        )
        .order_by("-total_products_sold")[:5]
    )

    # -----------------------------
    # Revenue KPIs
    # -----------------------------

    today = timezone.now().date()

    today_revenue = (
        Order.objects.filter(
            payment_status="Paid",
            created_at__date=today,
        ).aggregate(total=Sum("total_amount"))["total"] or 0
    )

    week_start = today - timedelta(days=7)

    week_revenue = (
        Order.objects.filter(
            payment_status="Paid",
            created_at__date__gte=week_start,
        ).aggregate(total=Sum("total_amount"))["total"] or 0
    )

    month_revenue = (
        Order.objects.filter(
            payment_status="Paid",
            created_at__year=today.year,
            created_at__month=today.month,
        ).aggregate(total=Sum("total_amount"))["total"] or 0
    )

    average_order_value = (
        Order.objects.filter(payment_status="Paid")
        .aggregate(avg=Avg("total_amount"))["avg"] or 0
    )

    # -----------------------------
    # Context
    # -----------------------------

    context = {

        # Summary
        "total_orders": total_orders,
        "total_products": total_products,
        "total_customers": total_customers,
        "total_revenue": total_revenue,

        # Order Status
        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "cancelled_orders": cancelled_orders,

        # Payment Status
        "paid_orders": paid_orders,
        "pending_payments": pending_payments,
        "failed_payments": failed_payments,

        # Low Stock
        "low_stock_products": low_stock_products,

        # Monthly Sales
        "months": json.dumps(months),
        "sales": json.dumps(sales),

        # Best Selling Products
        "best_selling_products": best_selling_products,

        # Top Customers
        "top_customers": top_customers,

        # Order Status Chart
        "order_status_data": json.dumps([
            pending_orders,
            processing_orders,
            shipped_orders,
            delivered_orders,
            cancelled_orders,
        ]),

        # Payment Status Chart
        "payment_status_data": json.dumps([
            paid_orders,
            pending_payments,
            failed_payments,
        ]),

        # Category Revenue Chart
        "category_names": json.dumps(category_names),
        "category_revenue": json.dumps(category_revenue),

        # Recent Orders
        "recent_orders": recent_orders,

        # Top Categories
        "top_categories": top_categories,

        # KPI Cards
        "today_revenue": today_revenue,
        "week_revenue": week_revenue,
        "month_revenue": month_revenue,
        "average_order_value": average_order_value,
    }

    return render(
        request,
        "analytics/dashboard.html",
        context,
    )