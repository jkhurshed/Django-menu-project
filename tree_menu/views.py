from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'tree_menu/home.html')

def about(request):
    return render(request, 'tree_menu/about.html')

def contact(request):
    return render(request, 'tree_menu/contact.html')
