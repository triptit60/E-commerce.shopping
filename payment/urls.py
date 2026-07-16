from django.urls import path
from .import views
urlpatterns = [
          path('payment', views.Payment_Success, name='payment_success'),
     
]   