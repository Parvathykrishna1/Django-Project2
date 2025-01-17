from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, Product, Sub_Category


# Create your views here.

def home(request):
    featured_categories = Sub_Category.objects.all().filter(is_featured=True)[:5]
    featured_products = Product.objects.all().filter(is_featured=True)[:2]
    off_products = Product.objects.filter(product_offer__gt=0)

    context = {
        "featured_categories": featured_categories,
        "featured_products": featured_products,
        "off_products": off_products,
    }

    return render(request, "main/home.html", context)


def etc(request, category_slug=None, sub_category_slug=None):
    categories_shop = None
    subCategories_shop = None
    products = None
    featured_categories = Sub_Category.objects.all().filter(is_featured=True)[:5]
    featured_products = Product.objects.all().filter(is_featured=True)  # [:1]
    off_products = Product.objects.filter(product_offer__gt=0)

    if sub_category_slug != None:
        subCategories_shop = get_object_or_404(Sub_Category, slug=sub_category_slug)
        products = Product.objects.all().filter(
            sub_category=subCategories_shop, is_available=True
        )
        product_count = products.count()

    elif category_slug != None:
        categories_shop = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(
            category=categories_shop, is_available=True
        )
        product_count = products.count()

    else:
        categories_shop = Category.objects.all()
        subCategories_shop = Sub_Category.objects.all()
        products = (
            Product.objects.all().filter(is_available=True).order_by("product_name")
        )
        product_count = products.count()

    if request.method == "POST":
        min = request.POST["minamount"]
        max = request.POST["maxamount"]
        min_price = min
        max_price = max
        products = (
            Product.objects.all()
            .filter(Q(price__gte=min_price), Q(price__lte=max_price), is_available=True)
            .order_by("price")
        )
        product_count = products.count()

    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "categories_shop": categories_shop,
        "subCategories_shop": subCategories_shop,
        "products": page_obj,
        "product_count": product_count,
        "featured_categories": featured_categories,
        "featured_products": featured_products,
        "off_products": off_products,
    }
    return render(request, "main/shop.html", context)


def product_details(request, category_slug, sub_category_slug, product_slug):
    categories = Category.objects.all()
    sub_category = Category.objects.all()

    try:
        product = Product.objects.get(
            category__slug=category_slug,
            sub_category__slug=sub_category_slug,
            slug=product_slug,
        )
        # in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=product).exists()
        related_products = Product.objects.filter(sub_category__slug=sub_category_slug)[
            :4
        ]

    except Exception as e:
        raise e

    context = {
        "sub_category": sub_category,
        "categories": categories,
        "product": product,
        "related_products": related_products,
        # "in_cart":in_cart,
    }
    return render(request, "main/product_detail.html", context)


def sub_category(request):
    cat_id = request.GET["category_id"]
    sub_categories = Sub_Category.objects.filter(category=cat_id).values()

    return JsonResponse(
        {
            "success": True,
            "sub_categories": list(sub_categories),
        },
        safe=False,
    )


def base(request):
    return render(request, "base.html")


def search(request):
    if request.method == "GET":
        keyword = request.GET["keyword"]
        if keyword:
            products = Product.objects.order_by("-created_date").filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
            product_count = products.count()

    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "products": page_obj,
        "product_count": product_count,
    }
    return render(request, "main/shop.html", context)


def handler404(request, exception):
    return render(request, "main/404.html")


def contact(request):
    return render(request, "main/contact.html")


def blog(request):
    return render(request, "main/blog.html")
