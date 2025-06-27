from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User   # <--- Add this line

def home_view(request):
    return render(request, 'home.html')
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')


def cart_view(request):
    return render(request, 'cart.html')
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate using email as username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect('home')  # Replace with your homepage or dashboard
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')
def signup_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        user.save()
        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')
    return render(request, 'signup.html')
def password_reset_view(request):
    return render(request, 'password_reset.html') 
def search_product_view(request):
    return render(request, 'searchproduct.html')
def account_view(request):
    return render(request, 'account.html')
def edit_profile_view(request):
    return render(request, 'editprofile.html')
def category_view(request):
    return render(request, 'category.html')
def customize_view(request):
    return render(request, 'customize.html')
def cart_view(request):
    return render(request, 'cart.html')
def placeorder_view(request):
    return render(request, 'placeorder.html')


