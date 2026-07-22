from django.shortcuts import render
from django.shortcuts import render, redirect
from products.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product, Profile
from django.db.models import Count, Sum, F, DecimalField, ExpressionWrapper, Value
from django.db.models.functions import Coalesce, TruncDate
from django.utils import timezone
from datetime import timedelta
import datetime
from decimal import Decimal


# Create your views here.
def Payment_Success(request):
    return render(request, 'payment/payment_success.html')


# def owner_dashboard(request):
# 	"""A live dashboard built from the project's existing orders and products."""
# 	if not (request.user.is_authenticated and request.user.is_superuser):
# 		messages.error(request, "Only store owners can access the dashboard.")
# 		return redirect('home')

# 	today = timezone.localdate()
# 	week_start = today - timedelta(days=6)
# 	orders = Order.objects.all()
# 	money_field = DecimalField(max_digits=12, decimal_places=2)
# 	zero_money = Value(Decimal('0.00'), output_field=money_field)
# 	recent_orders = orders.select_related('user').order_by('-date_ordered')[:7]
# 	weekly_sales = (orders.filter(date_ordered__date__gte=week_start).annotate(day=TruncDate('date_ordered')).values('day').annotate(total=Coalesce(Sum('amount_paid'), zero_money), order_count=Count('id')).order_by('day'))
# 	sales_by_day = {entry['day']: entry for entry in weekly_sales}
# 	chart_data = []
# 	for offset in range(7):
# 		day = week_start + timedelta(days=offset)
# 		entry = sales_by_day.get(day, {})
# 		chart_data.append({'label': day.strftime('%a'), 'total': entry.get('total', Decimal('0.00')), 'orders': entry.get('order_count', 0)})
# 	max_sales = max((item['total'] for item in chart_data), default=Decimal('1.00')) or Decimal('1.00')
# 	for item in chart_data:
# 		item['height'] = max(8, int((item['total'] / max_sales) * 100)) if item['total'] else 8

# 	top_products = (OrderItem.objects.values('product__name').annotate(units=Coalesce(Sum('quantity'), 0), revenue=Coalesce(Sum(ExpressionWrapper(F('price') * F('quantity'), output_field=money_field)), zero_money)).order_by('-units')[:5])
# 	return render(request, 'payment/owner_dashboard.html', {
# 		'total_revenue': orders.aggregate(total=Coalesce(Sum('amount_paid'), zero_money))['total'],
# 		'today_revenue': orders.filter(date_ordered__date=today).aggregate(total=Coalesce(Sum('amount_paid'), zero_money))['total'],
# 		'total_orders': orders.count(), 'pending_orders': orders.filter(shipped=False).count(),
# 		'shipped_orders': orders.filter(shipped=True).count(),
# 		'total_customers': User.objects.filter(is_superuser=False).count(),
# 		'total_products': Product.objects.count(), 'total_categories': Product.objects.values('category').distinct().count(),
# 		'chart_data': chart_data, 'recent_orders': recent_orders, 'top_products': top_products,
# 	})


def orders(request, pk):
	if request.user.is_authenticated and request.user.is_superuser:
		# Get the order
		order = Order.objects.get(id=pk)
		# Get the order items
		items = OrderItem.objects.filter(order=pk)

		if request.POST:
			status = request.POST['shipping_status']
			# Check if true or false
			if status == "true":
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				now = datetime.datetime.now()
				order.update(shipped=True, date_shipped=now)
			else:
				# Get the order
				order = Order.objects.filter(id=pk)
				# Update the status
				order.update(shipped=False)
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, 'payment/orders.html', {"order":order, "items":items})




	else:
		messages.success(request, "Access Denied")
		return redirect('home')




def not_shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=False)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# Get the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=True, date_shipped=now)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')

		return render(request, "payment/not_shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')



def shipped_dash(request):
	if request.user.is_authenticated and request.user.is_superuser:
		orders = Order.objects.filter(shipped=True)
		if request.POST:
			status = request.POST['shipping_status']
			num = request.POST['num']
			# grab the order
			order = Order.objects.filter(id=num)
			# grab Date and time
			now = datetime.datetime.now()
			# update order
			order.update(shipped=False)
			# redirect
			messages.success(request, "Shipping Status Updated")
			return redirect('home')


		return render(request, "payment/shipped_dash.html", {"orders":orders})
	else:
		messages.success(request, "Access Denied")
		return redirect('home')





def process_order(request):
	if request.POST:
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		# Get Billing Info from the last page
		payment_form = PaymentForm(request.POST or None)
		# Get Shipping Session Data
		my_shipping = request.session.get('my_shipping')

		# Gather Order Info
		full_name = my_shipping['shipping_full_name']
		email = my_shipping['shipping_email']
		# Create Shipping Address from session info
		shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
		amount_paid = totals

		# Create an Order
		if request.user.is_authenticated:
			# logged in
			user = request.user
			# Create Order
			create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, user=user, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]

			# Delete Cart from Database (old_cart field)
			current_user = Profile.objects.filter(user__id=request.user.id)
			# Delete shopping cart in database (old_cart field)
			current_user.update(old_cart="")


			messages.success(request, "Order Placed!")
			return redirect('home')

			

		else:
			# not logged in
			# Create Order
			create_order = Order(full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
			create_order.save()

			# Add order items
			
			# Get the order ID
			order_id = create_order.pk
			
			# Get product Info
			for product in cart_products():
				# Get product ID
				product_id = product.id
				# Get product price
				if product.is_sale:
					price = product.sale_price
				else:
					price = product.price

				# Get quantity
				for key,value in quantities().items():
					if int(key) == product.id:
						# Create order item
						create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
						create_order_item.save()

			# Delete our cart
			for key in list(request.session.keys()):
				if key == "session_key":
					# Delete the key
					del request.session[key]



			messages.success(request, "Order Placed!")
			return redirect('home')


	else:
		messages.success(request, "Access Denied")
		return redirect('home')




def billing_info(request):
	if request.POST:
		# Get the cart
		cart = Cart(request)
		cart_products = cart.get_prods
		quantities = cart.get_quants
		totals = cart.cart_total()

		# Create a session with Shipping Info
		my_shipping = request.POST
		request.session['my_shipping'] = my_shipping

		# # Get the host
		# host = request.get_host()
		# # Create Paypal Form Dictionary
		# paypal_dict = {
		# 	'business': settings.PAYPAL_RECEIVER_EMAIL,
		# 	'amount': totals,
		# 	'item_name': 'Book Order',
		# 	'no_shipping': '2',
		# 	'invoice': str(uuid.uuid4()),
		# 	'currency_code': 'USD', # EUR for Euros
		# 	'notify_url': 'https://{}{}'.format(host, reverse("paypal-ipn")),
		# 	'return_url': 'https://{}{}'.format(host, reverse("payment_success")),
		# 	'cancel_return': 'https://{}{}'.format(host, reverse("payment_failed")),
		# }

		# # Create acutal paypal button
		# paypal_form = PayPalPaymentsForm(initial=paypal_dict)


		# # Check to see if user is logged in
		# if request.user.is_authenticated:
		# 	# Get The Billing Form
		# 	billing_form = PaymentForm()
		# 	return render(request, "payment/billing_info.html", {"paypal_form":paypal_form, "cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})

		# else:
		# 	# Not logged in
		# 	# Get The Billing Form
		# 	billing_form = PaymentForm()
		# 	return render(request, "payment/billing_info.html", {"paypal_form":paypal_form, "cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})


		
		shipping_form = request.POST
		return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})	
	else:
		messages.success(request, "Access Denied")
		return redirect('home')


def checkout(request):
	# Get the cart
	cart = Cart(request)
	cart_products = cart.get_prods
	quantities = cart.get_quants
	totals = cart.cart_total()

	if request.user.is_authenticated:
		# Checkout as logged in user
		# Shipping User
		shipping_user = ShippingAddress.objects.filter(user=request.user).first()
		# Shipping Form
		shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
	else:
		# Checkout as guest
		shipping_form = ShippingForm(request.POST or None)
		return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

	

def payment_success(request):
	return render(request, "payment/payment_success.html", {})


def payment_failed(request):
	return render(request, "payment/payment_failed.html", {})
