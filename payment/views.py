
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.shortcuts import render
from products.cart import Cart
from django.contrib import messages
from payment.forms import ShippingForm
from payment.models import ShippingAddress, Order, OrderItem

# Create your views here.
def billing_info(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if not cart_products:
        messages.error(request, "Your cart is empty.")
        return redirect('cart_summary')

    if request.method == 'POST':
        if request.user.is_authenticated:
            shipping_user, _ = ShippingAddress.objects.get_or_create(user=request.user)
            shipping_form = ShippingForm(request.POST, instance=shipping_user)
        else:
            shipping_form = ShippingForm(request.POST)

        if shipping_form.is_valid():
            if request.user.is_authenticated:
                shipping_form.save()

            return render(request, "payment/billing_info.html", {
                "cart_products": cart_products,
                "quantities": quantities,
                "totals": totals,
                "shipping_info": shipping_form.cleaned_data,
            })

        return render(request, "payment/checkout.html", {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_form": shipping_form,
        })

    messages.warning(request, "Please complete shipping information first.")
    return redirect('checkout')


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





def Payment_Success(request):
    return render(request, 'payment/payment_success.html')


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()

    if request.user.is_authenticated:
        shipping_user, _ = ShippingAddress.objects.get_or_create(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    else:
        shipping_form = ShippingForm(request.POST or None)

    return render(request, "payment/checkout.html", {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form,
    })

   