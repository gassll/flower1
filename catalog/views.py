from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from .forms import ProductForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

def my_view(request):
    categories = Category.objects.all()
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


