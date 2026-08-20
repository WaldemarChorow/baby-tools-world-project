from typing import Optional

from django.contrib import messages
from django.db.models import Avg, Count, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import CommentForm
from .models import Category, Comment, Product


def product_list(request: HttpRequest, category_slug: Optional[str] = None) -> HttpResponse:
    """Display list of all products, optionally filtered by category.

    Args:
        request: The HTTP request object
        category_slug: Optional slug for filtering products by category

    Returns:
        HttpResponse: Rendered products.html template with categories and products
    """
    categories: QuerySet[Category] = Category.objects.all()
    products: QuerySet[Product] = Product.objects.select_related("category").annotate(
        avg_rating=Avg("comments__rating"), total_ratings=Count("comments")
    )
    if category_slug:
        products = products.filter(category__slug=category_slug)
    return render(request, "products.html", {"categories": categories, "products": products})


def product_detail(request: HttpRequest, category_slug: str, pk: int) -> HttpResponse:
    """Display detailed information about a specific product with comments and ratings.

    Handles both GET requests (display form) and POST requests (submit new comment).
    After successful comment submission, the form is reset and comments are refreshed.

    Args:
        request: The HTTP request object (GET or POST)
        category_slug: The slug of the product's category
        pk: The primary key (ID) of the product

    Returns:
        HttpResponse: Rendered product.html template with product details, comments,
                     related products, and comment form
    """
    product = get_object_or_404(
        Product.objects.select_related("category").annotate(
            avg_rating=Avg("comments__rating"), total_ratings=Count("comments")
        ),
        pk=pk,
        category__slug=category_slug,
    )

    related_products: QuerySet[Product] = (
        Product.objects.filter(category=product.category)
        .exclude(pk=product.pk)
        .annotate(avg_rating=Avg("comments__rating"), total_ratings=Count("comments"))
        .order_by("-avg_rating", "-total_ratings", "name")[:8]
    )

    comments: QuerySet[Comment] = product.comments.select_related("user").order_by("-created_at")

    if request.method == "POST":
        form: CommentForm = CommentForm(
            request.POST, initial={"user": request.user if request.user.is_authenticated else None}
        )
        if form.is_valid():
            rating: int = form.cleaned_data["rating"]
            text: str = form.cleaned_data.get("text", "")

            if request.user.is_authenticated:
                # Upsert: update existing comment or create a new one
                comment, created = Comment.objects.get_or_create(
                    product=product, user=request.user, defaults={"rating": rating, "text": text}
                )
                if not created:
                    comment.rating = rating
                    comment.text = text
                    comment.save()
                messages.success(request, "Your rating was {}.".format("submitted" if created else "updated"))
            else:
                # Guest: create a new comment (no uniqueness constraint)
                comment = form.save(commit=False)
                comment.product = product
                comment.save()
                messages.success(request, "Thank you for your rating.")

            comments = product.comments.select_related("user").order_by("-created_at")
            form = CommentForm()
            return render(
                request,
                "product.html",
                {"product": product, "comments": comments, "related_products": related_products, "form": form},
            )
    else:
        # Pre-fill form for authenticated user with existing comment (if any)
        initial: dict = {}
        if request.user.is_authenticated:
            existing: Optional[Comment] = product.comments.filter(user=request.user).first()
            if existing:
                initial = {"rating": existing.rating, "text": existing.text}
        form: CommentForm = CommentForm(initial=initial)

    return render(
        request,
        "product.html",
        {"product": product, "comments": comments, "related_products": related_products, "form": form},
    )
