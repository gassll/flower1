from django.shortcuts import render
from .models import Category


def my_view(request):
    category = Category.objects.first()
    return render(request, 'index.html', {'category': category})

def category_view(request):
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories})

def category_detail(request, pk):
    category = Category.objects.get(pk=pk)
    return render(request, 'index.html', {'category': category, 'categories': Category.objects.all()})