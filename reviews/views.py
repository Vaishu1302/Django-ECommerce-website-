from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from products.models import Product
from .models import Review
from .forms import ReviewForm
from django.core.paginator import Paginator

@login_required
def add_review(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    review = Review.objects.filter(
        user=request.user,
        product=product
    ).first()

    if review:
        return redirect(
            "edit_review",
            review.id
        )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            new_review = form.save(
                commit=False
            )

            new_review.user = request.user

            new_review.product = product

            new_review.save()

            return redirect(
                "product_detail",
                product.id
            )

    else:

        form = ReviewForm()

    return render(
        request,
        "reviews/add_review.html",
        {
            "form": form,
            "product": product,
        }
    )


@login_required
def edit_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    if request.method == "POST":

        form = ReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():

            form.save()

            return redirect(
                "product_detail",
                review.product.id
            )

    else:

        form = ReviewForm(
            instance=review
        )

    return render(
        request,
        "reviews/edit_review.html",
        {
            "form": form,
            "review": review,
        }
    )


@login_required
def delete_review(request, review_id):

    review = get_object_or_404(
        Review,
        id=review_id,
        user=request.user
    )

    if request.method == "POST":

        product_id = review.product.id

        review.delete()

        return redirect(
            "product_detail",
            product_id
        )

    return render(
        request,
        "reviews/delete_review.html",
        {
            "review": review,
        }
    )