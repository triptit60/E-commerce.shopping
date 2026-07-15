from django.urls import path
from .import views


urlpatterns = [
        path('product/<int:pk>', views.Products, name='product'),
        path('category/<str:foo>', views.category, name='category'),
        path('category_summary/', views.category_summary, name='category_summary'),

        
        #cart 
        path('', views.cart_summary, name="cart_summary"),
	path('add/', views.cart_add, name="cart_add"),
	path('delete/', views.cart_delete, name="cart_delete"),
	path('update/', views.cart_update, name="cart_update"),

]
               
