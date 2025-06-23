from django.shortcuts import render,redirect


def home_view(request):
    return render(request, 'home.html')


def cart_view(request):
    return render(request, 'cart.html')
def login_view(request):
    return render(request, 'login.html')
def signup_view(request):
    return render(request, 'signup.html')
def password_reset_view(request):
    return render(request, 'password_reset.html') 
def search_product_view(request):
    return render(request, 'searchproduct.html')