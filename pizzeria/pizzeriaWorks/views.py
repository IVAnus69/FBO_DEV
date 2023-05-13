from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from .models import Pizza, Specifications


def index(request):
    return render(request, 'index.html')

def registration(request):
    return render(request, 'registration.html')

def product_view(request):
    products = Pizza.objects.all()
    print(products)
    return render(request, 'product.html', {'products' : products})

def product_detail_view(request, pk):
    product = get_object_or_404(Pizza, pk=pk)
    product_spec = Specifications.objects.all().filter(pizza_id = product.id)
    return render(request, 'product_detail.html', {'product': product,
                                                   'product_spec' : product_spec})