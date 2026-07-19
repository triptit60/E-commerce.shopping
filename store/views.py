from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q, Sum
from payment.models import Order, OrderItem

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


@staff_member_required
def admin_dashboard(request):
	total_products = Product.objects.count()
	total_categories = Category.objects.count()
	total_orders = Order.objects.count()
	# Count registered store customers (Profile is created on user signup)
	total_customers = Profile.objects.count()
	total_revenue = Order.objects.aggregate(total=Sum('amount_paid'))['total'] or 0
	recent_orders = Order.objects.select_related('user').order_by('-date_ordered')[:10]
	top_products = (
		OrderItem.objects.values('product__name')
		.annotate(total_sold=Sum('quantity'))
		.order_by('-total_sold')[:5]
	)

	return render(request, 'store/admin_dashboard.html', {
		'total_products': total_products,
		'total_categories': total_categories,
		'total_orders': total_orders,
		'total_customers': total_customers,
		'total_revenue': total_revenue,
		'recent_orders': recent_orders,
		'top_products': top_products,
	})
