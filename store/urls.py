from django.urls import path
from .import views
urlpatterns = [
          path('', views.home, name='home'),
          path('about/', views.about, name='about'),
          path('search/', views.search, name='search'),
          path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]         

    