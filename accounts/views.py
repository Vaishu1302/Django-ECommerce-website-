from django.shortcuts import render
import random
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.shortcuts import get_object_or_404


from django.shortcuts import redirect
from django.shortcuts import render
from .forms import RegisterForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages

from django.db.models import Sum
from products.models import Product, Category
from orders.models import OrderItem
def home(request):

    # Hero Section
    featured_products = Product.objects.all()[:4]

    # New Arrivals
    new_arrivals = Product.objects.order_by("-created_at")[:8]

    # Best Selling Products
    best_selling_products = (
        Product.objects
        .annotate(
            total_sold=Sum("orderitem__quantity")
        )
        .order_by("-total_sold")[:8]
    )

    # Categories
    categories = Category.objects.all()

    context = {

        "featured_products": featured_products,

        "new_arrivals": new_arrivals,

        "best_selling_products": best_selling_products,

        "categories": categories,

    }

    return render(
        request,
        "accounts/home.html",
        context
    )


def register(request):

    print("METHOD:", request.method)

    if request.method == "POST":

        print(request.POST)

        form = RegisterForm(request.POST)

        if form.is_valid():

            print("VALID FORM")

            user = form.save()

            print("USER CREATED")

            login(request, user)

            return redirect("home")

        else:

            print("ERRORS:", form.errors)

    else:

        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {"form": form}
    )


def user_login(request):

    print("METHOD:", request.method)

    if request.method == "POST":

        print(request.POST)

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():

            print("LOGIN SUCCESS")

            login(request, form.get_user())

            return redirect("home")

        else:

            print(form.errors)

    else:

        form = AuthenticationForm()

    return render(request, "accounts/login.html", {"form": form})

def user_logout(request):

    logout(request)

    return redirect('login')





@login_required
def profile(request):

    return render(

        request,

        'accounts/profile.html',

        {

            'profile': request.user.userprofile

        }

    )



@login_required
def edit_profile(request):

    profile = request.user.userprofile

    if request.method == "POST":

        form = ProfileForm(

            request.POST,

            request.FILES,

            instance=profile

        )

        if form.is_valid():

            form.save()

            return redirect(
                'profile'
            )

    else:

        form = ProfileForm(
            instance=profile
        )

    return render(

        request,

        'accounts/edit_profile.html',

        {

            'form': form

        }

    )
def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email")

        try:

            user = User.objects.get(email=email)

        except User.DoesNotExist:

            messages.error(request, "Email not registered.")

            return redirect("forgot_password")

        otp = str(random.randint(100000, 999999))

        request.session["reset_email"] = email
        request.session["reset_otp"] = otp

        send_mail(
            "Password Reset OTP",
            f"Your OTP is {otp}",
            "yourgmail@gmail.com",
            [email],
            fail_silently=False,
        )

        return redirect("verify_otp")

    return render(
        request,
        "accounts/forgot_password.html"
    )


def verify_otp(request):

    if request.method == "POST":

        otp = request.POST.get("otp")

        if otp == request.session.get("reset_otp"):

            return redirect("reset_password")

        messages.error(request, "Invalid OTP")

    return render(
        request,
        "accounts/verify_otp.html"
    )


def reset_password(request):

    if request.method == "POST":

        password = request.POST.get("password")

        confirm = request.POST.get("confirm_password")

        if password != confirm:

            messages.error(request, "Passwords do not match")

            return redirect("reset_password")

        email = request.session.get("reset_email")

        user = User.objects.get(email=email)

        user.set_password(password)

        user.save()

        request.session.flush()

        messages.success(request, "Password changed successfully.")

        return redirect("login")

    return render(
        request,
        "accounts/reset_password.html"
    )
def home(request):
    return render(request, "accounts/home.html")
# def product_list(request):

#     products = Product.objects.all()

#     return render(
#         request,
#         "products/product_list.html",
#         {
#             "products": products
#         }
#     )


# def product_detail(request, pk):

#     product = get_object_or_404(
#         Product,
#         id=pk
#     )

#     return render(
#         request,
#         "products/product_detail.html",
#         {
#             "product": product
#         }
#     )