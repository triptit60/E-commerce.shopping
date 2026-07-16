from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.db.models import Q

def home(request):
    products = Product.objects.all()
    return render(request, 'store/homepage.html', {'products' :products})

def  about(request):
    return render(request, 'store/about.html',{})

from django.shortcuts import redirect


def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		searched = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
		# Test for null
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "store/search.html", {})
		else:
			return render(request, "store/search.html", {'searched':searched})
	else:
		return render(request, "store/search.html", {})	
