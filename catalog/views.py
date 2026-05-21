from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Order
from .forms import ProductForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Favorite, Cart
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .decorators import manager_or_admin_required


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
    query = request.GET.get('q', '').strip()

    products = Product.objects.filter(is_available=True).select_related('category')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(name__icontains=query.lower()) |
            Q(name__icontains=query.upper()) |
            Q(name__icontains=query.capitalize())
        )

    if category_id:
        products = products.filter(category_id=category_id)

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
        'query': query,
        'user_favorites': user_favorites,
        'current_get': request.GET,
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

    if not items.exists():
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('catalog')

    return render(request, 'catalog/checkout.html', {
        'items': items,
        'total': total,
        'cart_count': get_cart_count(request.user),
        'today': timezone.now().date(),
    })


@login_required
def create_order(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user)

        if not cart_items.exists():
            messages.error(request, 'Ваша корзина пуста')
            return redirect('cart')

        items_data = []
        for item in cart_items:
            items_data.append({
                'product_id': item.product.id,
                'product_name': item.product.name,
                'product_price': float(item.product.price),
                'quantity': item.quantity,
                'total': float(item.product.price * item.quantity)
            })

        order = Order.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            comment=request.POST.get('comment', ''),
            payment_method=request.POST.get('payment_method'),
            delivery_date=request.POST.get('delivery_date'),
            delivery_time=request.POST.get('delivery_time'),
            cart_items=items_data,  # Сохраняем состав заказа
            total_sum=sum(item.product.price * item.quantity for item in cart_items),
            user=request.user
        )

        cart_items.delete()

        request.session['last_order_id'] = order.id

        messages.success(request, f'Заказ #{order.id} успешно оформлен!')

        return redirect('order_success')

    return redirect('checkout')


@login_required
def order_success(request):
    order_id = request.session.get('last_order_id')
    order = None

    if order_id:
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            pass

    return render(request, 'catalog/order_success.html', {
        'order': order,
        'cart_count': get_cart_count(request.user),
    })


@login_required
def profile(request):
    """Главная страница личного кабинета"""
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    total_orders = Order.objects.filter(user=request.user).count()
    favorites_count = Favorite.objects.filter(user=request.user).count()
    cart_count = Cart.objects.filter(user=request.user).count()

    context = {
        'user': request.user,
        'recent_orders': recent_orders,
        'total_orders': total_orders,
        'favorites_count': favorites_count,
        'cart_count': cart_count,
        'section': 'dashboard'
    }
    return render(request, 'catalog/profile_dashboard.html', context)


@login_required
def profile_orders(request):
    """Список всех заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
        'cart_count': get_cart_count(request.user),
        'section': 'orders'
    }
    return render(request, 'catalog/profile_orders.html', context)


@login_required
def profile_order_detail(request, order_id):
    """Детальная информация о заказе"""
    order = get_object_or_404(Order, id=order_id, user=request.user)

    context = {
        'order': order,
        'cart_count': get_cart_count(request.user),
        'section': 'orders'
    }
    return render(request, 'catalog/profile_order_detail.html', context)


@login_required
def profile_edit(request):
    """Редактирование профиля пользователя"""
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        messages.success(request, 'Профиль успешно обновлен!')
        return redirect('profile')

    context = {
        'user': request.user,
        'cart_count': get_cart_count(request.user),
        'section': 'profile'
    }
    return render(request, 'catalog/profile_edit.html', context)


@login_required
def change_password(request):
    """Изменение пароля"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('profile')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
        'cart_count': get_cart_count(request.user),
        'section': 'password'
    }
    return render(request, 'catalog/change_password.html', context)


@login_required
def profile_favorites(request):
    """Избранные товары пользователя"""
    favorites = Favorite.objects.filter(user=request.user).select_related('product')

    context = {
        'favorites': favorites,
        'cart_count': get_cart_count(request.user),
        'section': 'favorites'
    }
    return render(request, 'catalog/profile_favorites.html', context)


@manager_or_admin_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    form = ProductForm(request.POST or None, request.FILES or None, instance=product)

    if form.is_valid():
        form.save()
        return redirect('catalog')

    return render(request, 'catalog/edit_product.html', {'form': form})


@manager_or_admin_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        product.delete()
        return redirect('catalog')

    return render(request, 'catalog/delete_product.html', {'product': product})
