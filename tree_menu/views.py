from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'tree_menu/home.html')

def about(request):
    return render(request, 'tree_menu/about.html')

def contact(request):
    return render(request, 'tree_menu/contact.html')

def web_development(request):
    return render(request, 'tree_menu/web_development.html')

def mobile_development(request):
    return render(request, 'tree_menu/mobile_development.html')

def products(request):
    return render(request, 'tree_menu/products.html')

def support(request):
    return render(request, 'tree_menu/support.html')
