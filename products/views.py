from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Product, Category
from .forms import ProductForm, CategoryForm
from django.db.models import Avg
from reviews.models import Review
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_staff
# -----------------------------
# Product List (Everyone)
# -----------------------------
from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request):

    products = Product.objects.all()
    categories = Category.objects.all()

    search = request.GET.get("search")

    if search:
        products = products.filter(name__icontains=search)

    category = request.GET.get("category")

    if category:
        products = products.filter(category_id=category)

    min_price = request.GET.get("min_price")

    if min_price:
        products = products.filter(price__gte=min_price)

    max_price = request.GET.get("max_price")

    if max_price:
        products = products.filter(price__lte=max_price)

    sort = request.GET.get("sort")

    if sort == "low":
        products = products.order_by("price")

    elif sort == "high":
        products = products.order_by("-price")

        # Pagination
    paginator = Paginator(products, 8)   # Show 8 products per page

    page_number = request.GET.get("page")

    products = paginator.get_page(page_number)

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
        }
    )



def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    # Related Products
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    # -----------------------------
    # Recently Viewed Products
    # -----------------------------

    viewed = request.session.get("recently_viewed", [])

    # Remove current product if already exists
    if product.id in viewed:
        viewed.remove(product.id)

    # Add current product at the beginning
    viewed.insert(0, product.id)

    # Keep only last 5 products
    viewed = viewed[:5]

    request.session["recently_viewed"] = viewed

    recently_viewed = Product.objects.filter(
        id__in=viewed
    ).exclude(
        id=product.id
    )
    # -----------------------------
# Product Reviews Pagination
# -----------------------------

    reviews = Review.objects.filter(
        product=product
    ).select_related(
        "user"
    ).order_by("-created_at")

    paginator = Paginator(
        reviews,
        5      # 5 reviews per page
    )

    page_number = request.GET.get("page")

    reviews = paginator.get_page(page_number)

    context = {
    "product": product,

    "related_products": related_products,

    "recently_viewed": recently_viewed,

    "reviews": reviews,




    }

    return render(
        request,
        "products/product_detail.html",
        context
    )
# -----------------------------
# Add Product (Admin Only)
# -----------------------------
@staff_member_required(login_url='login')
def add_product(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            return redirect("product_list")

    else:

        form = ProductForm()

    return render(
        request,
        "products/add_product.html",
        {
            "form": form
        }
    )


# -----------------------------
# Edit Product (Admin Only)
# -----------------------------
@staff_member_required(login_url='login')
def edit_product(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            form.save()

            return redirect(
                "product_detail",
                pk=product.id
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "products/edit_product.html",
        {
            "form": form,
            "product": product
        }
    )


# -----------------------------
# Delete Product (Admin Only)
# -----------------------------
@staff_member_required(login_url='login')
def delete_product(request, pk):

    product = get_object_or_404(
        Product,
        id=pk
    )

    if request.method == "POST":

        product.delete()

        return redirect(
            "product_list"
        )

    return render(
        request,
        "products/delete_product.html",
        {
            "product": product
        }
    )
@login_required
@user_passes_test(is_admin)
def category_list(request):

    categories = Category.objects.all()

    return render(
        request,
        "products/category_list.html",
        {
            "categories": categories
        }
    )
@login_required
@user_passes_test(is_admin)
def add_category(request):

    if request.method == "POST":

        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("category_list")

    else:

        form = CategoryForm()

    return render(
        request,
        "products/add_category.html",
        {
            "form": form
        }
    )
@login_required
@user_passes_test(is_admin)
def edit_category(request, pk):

    category = get_object_or_404(Category, id=pk)

    if request.method == "POST":

        form = CategoryForm(
            request.POST,
            instance=category
        )

        if form.is_valid():

            form.save()

            return redirect("category_list")

    else:

        form = CategoryForm(instance=category)

    return render(
        request,
        "products/edit_category.html",
        {
            "form": form,
            "category": category
        }
    )
@login_required
@user_passes_test(is_admin)
def delete_category(request, pk):

    category = get_object_or_404(Category, id=pk)

    if request.method == "POST":

        category.delete()

        return redirect("category_list")

    return render(
        request,
        "products/delete_category.html",
        {
            "category": category
        }
    )