from django.shortcuts import render

# Create your views here.
def Payment_Success(request):
    return render(request, 'payment/payment_success.html')
