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


# def category_detail(request, slug):
#     categories = Category.objects.all().order_by('name')
#
#     selected_category = get_object_or_404(
#         Category,
#         slug=slug
#     )
#
#     products = Product.objects.filter(
#         category=selected_category,
#         is_available=True
#     )
#
#     return render(request, 'catalog.html', {
#         'categories': categories,
#         'selected_category': selected_category,
#         'products': products,
#     })


# def catalog(request):
#     categories = Category.objects.all().order_by('name')
#
#     products = Product.objects.filter(
#         is_available=True
#     ).select_related('category')
#
#     return render(request, 'catalog.html', {
#         'categories': categories,
#         'products': products,
#         'selected_category': None,
#     })

def catalog(request):
    categories = Category.objects.all().order_by('name')

    products = Product.objects.filter(
        is_available=True
    ).select_related('category')

    return render(request, 'catalog.html', {
        'categories': categories,
        'products': products,
        'category_slug': None,
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

    return render(request, 'catalog.html', {  # ← обратно 'catalog.html'
        'categories': categories,
        'products': products,
        'category_slug': slug,
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


def kompanijam(request):
    return render(request, 'kompanijam.html')


def dostavka_i_oplata(request):
    return render(request, 'dostavka-i-oplata.html')


def politika_konfidentsialnosti(request):
    return render(request, 'politika-konfidentsialnosti.html')


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'catalog/product_detail.html', {
        'product': product
    })
