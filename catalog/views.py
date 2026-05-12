from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import ProductForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test


def my_view(request):
    categories = Category.objects.filter(is_featured=True)
    recommended_products = Product.objects.filter(is_recommended=True)

    return render(request, 'index.html', {
        'categories': categories,
        'recommended_products': recommended_products,
    })


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)

    return render(request, 'category_detail.html', {
        'category': category,
        'products': products,
    })


def catalog(request):
    products = Product.objects.all()

    return render(request, 'catalog.html', {
        'products': products,
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
    return render(request, 'about.html')


# def dish_list(request):
#     search_query = request.GET.get('search', '')
#     dishes = Dish.objects.all()
#
#     if search_query:
#         dishes = dishes.filter(name__icontains=search_query)
#
#     context = {
#         'dishes': dishes,
#         'search_query': search_query
#     }
#     return render(request, 'dishes.html', context)

def avtorskie_bukety(request):
    category = Category.objects.get(slug='avtorskie-bukety')
    products = Product.objects.filter(category=category)
    return render(request, 'catalog/avtorskie-bukety.html', {'products': products})


def vazy(request):
    category = Category.objects.get(slug='vazy')
    products = Product.objects.filter(category=category)
    return render(request, 'catalog/vazy.html', {'products': products})


def mono_duo_trio_bukety(request):
    category = Category.objects.get(slug='mono-duo-trio-bukety')
    products = Product.objects.filter(category=category)
    return render(request, 'catalog/mono-duo-trio-bukety.html', {'products': products})


def korzini_cvetov(request):
    category = Category.objects.get(slug='korzini-cvetov')
    products = Product.objects.filter(category=category)
    return render(request, 'catalog/korzini-cvetov.html', {'products': products})


def tsvety_v_korobkah(request):
    category = Category.objects.get(slug='tsvety-v-korobkah')
    products = Product.objects.filter(category=category)
    return render(request, 'catalog/tsvety-v-korobkah.html', {'products': products})


def kompanijam(request):
    return render(request, 'kompanijam.html')


def dostavka_i_oplata(request):
    return render(request, 'dostavka-i-oplata.html')

def politika_konfidentsialnosti(request):
    return render(request, 'politika-konfidentsialnosti.html')


def product_detail(request, id):
    product = Product.objects.get(id=id)

    return render(request, 'catalog/product_detail.html', {
        'product': product
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    return render(request, 'category_detail.html', {
        'category': category,
        'products': products
    })