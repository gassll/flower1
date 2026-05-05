from django.shortcuts import render

from catalog.models import Category


def my_view(request):
    category = Category.objects.first()
    return render(request, 'index.html', {'category': category})