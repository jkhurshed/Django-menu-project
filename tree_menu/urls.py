from django.urls import path
from . import views

app_name = 'tree_menu'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/web/', views.web_development, name='web_development'),
    path('services/mobile/', views.mobile_development, name='mobile_development'),
    path('products/', views.products, name='products'),
    path('support/', views.support, name='support'),
] 