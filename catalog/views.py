from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import ProductForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Favorite, Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def my_view(request):
    categories = Category.objects.filter(is_featured=True).order_by('name')
    recommended_products = Product.objects.filter(is_recommended=True)

    user_favorites = []

    if request.user.is_authenticated:
        user_favorites = [
            fav.product for fav in Favorite.objects.filter(user=request.user)
        ]

    return render(request, 'index.html', {
        'categories': categories,
        'recommended_products': recommended_products,
        'user_favorites': user_favorites,
    })


def catalog(request):
    categories = Category.objects.all().order_by('name')

    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(is_available=True).select_related('category')

    # категория
    if category_id:
        products = products.filter(category_id=category_id)

    # цена
    if min_price:
        try:
            products = products.filter(price__gte=int(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            products = products.filter(price__lte=int(max_price))
        except ValueError:
            pass

    user_favorites = []
    if request.user.is_authenticated:
        user_favorites = [f.product for f in Favorite.objects.filter(user=request.user)]

    return render(request, 'catalog.html', {
        'categories': categories,
        'products': products,
        'category_id': category_id,
        'min_price': min_price,
        'max_price': max_price,
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
