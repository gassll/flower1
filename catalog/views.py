from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import ProductForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Favorite, Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def my_view(request):
    categories = Category.objects.filter(is_featured=True)
    recommended_products = Product.objects.filter(is_recommended=True)
    user_favorites = []

    if request.user.is_authenticated:
        user_favorites = [
            fav.product for fav in Favorite.objects.filter(user=request.user)
        ]

    return render(request, 'index.html', {
        'categories': categories,
        'recommended_products': recommended_products,
        'cart_count': get_cart_count(request.user),
        'user_favorites': user_favorites,
    })


def catalog(request):
    categories = Category.objects.all().order_by('name')

    query = (request.GET.get('q') or '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(
        is_available=True
    ).select_related('category')

    # Валидация минимальной цены
    if min_price:
        try:
            min_price = int(min_price)
            if min_price < 1:
                min_price = 1  # Принудительно устанавливаем 1, если ввели меньше
        except ValueError:
            min_price = None

    # Валидация максимальной цены
    if max_price:
        try:
            max_price = int(max_price)
            if max_price < 0:
                max_price = None
        except ValueError:
            max_price = None

    # Применяем фильтры
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    user_favorites = []

    if request.user.is_authenticated:
        user_favorites = [
            fav.product for fav in Favorite.objects.filter(user=request.user)
        ]

    # Применяем поиск
    if query:
        query = query.strip().lower()
        products = [
            p for p in products
            if query in p.name.lower()
               or (p.description and query in p.description.lower())
               or (p.category and query in p.category.name.lower())
        ]

    return render(request, 'catalog.html', {
        'categories': categories,
        'products': products,
        'category_slug': None,
        'query': query,
        'user_favorites': user_favorites,
        'min_price': min_price,
        'max_price': max_price,
    })


def category_detail(request, slug):
    categories = Category.objects.all().order_by('name')

    selected_category = get_object_or_404(
        Category,
        slug=slug
    )

    products = Product.objects.filter(
        category=selected_category,
        is_available=True
    )

    user_favorites = []

    if request.user.is_authenticated:
        user_favorites = [
            fav.product for fav in Favorite.objects.filter(user=request.user)
        ]

    return render(request, 'catalog.html', {
        'categories': categories,
        'products': products,
        'category_slug': slug,
        'cart_count': get_cart_count(request.user),
        'user_favorites': user_favorites,
    })


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def add_product(request):
    form = ProductForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('catalog')

    return render(request, 'catalog/add_product.html', {'form': form})


def about(request):
    return render(request, 'about.html', {
        'cart_count': get_cart_count(request.user),
    })


def kompanijam(request):
    return render(request, 'kompanijam.html', {
        'cart_count': get_cart_count(request.user),
    })


def dostavka_i_oplata(request):
    return render(request, 'dostavka-i-oplata.html', {
        'cart_count': get_cart_count(request.user),
    })


def politika_konfidentsialnosti(request):
    return render(request, 'politika-konfidentsialnosti.html', {
        'cart_count': get_cart_count(request.user),
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'cart_count': get_cart_count(request.user),
    })


@login_required
def add_to_favorites(request, product_id):
    if request.method == 'POST':

        product = get_object_or_404(Product, id=product_id)

        favorite = Favorite.objects.filter(
            user=request.user,
            product=product
        )

        if favorite.exists():
            favorite.delete()
        else:
            Favorite.objects.create(
                user=request.user,
                product=product
            )

    return redirect(request.META.get('HTTP_REFERER', 'catalog'))


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    from django.urls import reverse

    return redirect(reverse('catalog'))


def get_cart_count(user):
    if user.is_authenticated:
        return Cart.objects.filter(user=user).count()
    return 0


@login_required
def favorites(request):
    favorites = Favorite.objects.filter(user=request.user)

    return render(request, 'catalog/favorites.html', {
        'favorites': favorites,
        'cart_count': get_cart_count(request.user),
    })


@login_required
def cart(request):
    items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'catalog/cart.html', {
        'items': items,
        'total': total,
        'cart_count': get_cart_count(request.user),
    })


@login_required
def cart_increase(request, product_id):
    item = Cart.objects.get(user=request.user, product_id=product_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def cart_decrease(request, product_id):
    item = Cart.objects.get(user=request.user, product_id=product_id)

    item.quantity -= 1
    if item.quantity <= 0:
        item.delete()
    else:
        item.save()

    return redirect('cart')


@login_required
def cart_remove(request, product_id):
    Cart.objects.filter(user=request.user, product_id=product_id).delete()
    return redirect('cart')


@login_required
def checkout(request):
    items = Cart.objects.filter(user=request.user)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'catalog/checkout.html', {
        'items': items,
        'total': total,
        'cart_count': get_cart_count(request.user),
    })
