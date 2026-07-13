from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 

def home(request):
    products = Product.objects.all()
    return render(request, 'store/homepage.html', {'products' :products})

def  about(request):
    return render(request, 'store/about.html',{})

