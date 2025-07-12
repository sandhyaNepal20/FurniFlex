from django.shortcuts import get_object_or_404, render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import Category, Product  # Import Product model
import json
from .models import UserProfile  # ✅ Add this at the top
from django.contrib.auth.hashers import make_password

from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.models import User   # <--- Add this line
from django.shortcuts import render, redirect
from django.core.mail import send_mail
import random
from django.conf import settings
from .models import Payment  # Make sure you have this model
from django.views.decorators.csrf import csrf_exempt

from django.db.models import Q

def home_view(request):
    products = Product.objects.all()[:4]  # Fetch only top 4 for homepage
    categories = Category.objects.all()  # corrected variable name to plural 'categories'

    return render(request, 'home.html', {'products': products, 'categories': categories})

    return render(request, 'home.html', {'products': products})
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('home')
def wishlist_view(request):
    return render(request, 'wishlist.html')
def beforecart_view(request):
    return render(request, 'beforecart.html')
def cart_view(request):
    return render(request, 'cart.html')
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            # 👇 Instead of redirecting immediately
            return render(request, 'login.html', {'redirect_after_login': True})
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

        # ✅ Create UserProfile and save phone
        profile = UserProfile.objects.create(user=user, phone=phone)
        profile.save()

        messages.success(request, "Account created successfully. Please log in.")
        return redirect('login')

    return render(request, 'signup.html')

def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        request.session['reset_email'] = email
        request.session['reset_otp'] = otp

        # Send email
        subject = 'FurniFlex Password Reset OTP'
        message = f'Your OTP for resetting your password is: {otp}'
        from_email = None  # Uses DEFAULT_FROM_EMAIL in settings
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return redirect('reset_code')

    return render(request, 'password_reset.html')
def reset_code_view(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        actual_otp = request.session.get('reset_otp')

        if user_otp == actual_otp:
            return redirect('set_new_password')  # create this view/page for new password input
        else:
            return render(request, 'resetcode.html', {'error': 'Invalid OTP. Try again.'})

    return render(request, 'resetcode.html')

def set_new_password_view(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'setnewpassword.html', {'error': 'Passwords do not match'})

        email = request.session.get('reset_email')
        if not email:
            return redirect('password_reset')  # Start over if no email in session

        try:
            user = User.objects.get(email=email)
            user.password = make_password(password1)
            user.save()

            # Clear session
            request.session.flush()

            return render(request, 'setnewpassword.html', {'success': 'Password changed successfully!'})
        except User.DoesNotExist:
            return render(request, 'setnewpassword.html', {'error': 'User not found'})

    return render(request, 'setnewpassword.html')
def search_product_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()  # corrected variable name to plural 'categories'

    for product in products:
        try:
            product.color_options = json.loads(product.color_options or "[]")
        except:
            product.color_options = []
    return render(request, 'searchproduct.html', {'products': products, 'categories': categories})
@login_required
def account_view(request):
    user = request.user
    try:
        phone = user.userprofile.phone
    except UserProfile.DoesNotExist:
        phone = "Not Provided"

    context = {
        'name': user.first_name,
        'email': user.email,
        'phone': phone
    }
    return render(request, 'account.html', context)
@login_required
def edit_profile_view(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        full_name = request.POST.get('fullname')
        phone = request.POST.get('phone')

        user.first_name = full_name
        user.save()

        profile.phone = phone
        profile.save()

        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if current_password or new_password or confirm_password:
            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect.")
                return redirect('editprofile')

            if new_password != confirm_password:
                messages.error(request, "New passwords do not match.")
                return redirect('editprofile')

            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Password updated successfully.")
        else:
            messages.success(request, "Profile updated successfully.")

      

    context = {
        'name': user.first_name,
        'email': user.email,
        'phone': profile.phone,
    }
    return render(request, 'editprofile.html', context)

def searchproduct_view(request):
    category_name = request.GET.get('type')  # Category from dropdown
    search_query = request.GET.get('q')  # Optional: from search bar

    categories = Category.objects.all().order_by('name')
    products = Product.objects.all()

  

    if category_name and category_name.lower() != "all":
        products = products.filter(category__name__iexact=category_name)

    for product in products:
        try:
            product.color_options = json.loads(product.color_options or "[]")
        except:
            product.color_options = []

    return render(request, 'searchproduct.html', {
        'products': products,
        'categories': categories,
        'selected_category': category_name,
        'search_query': search_query,
    })

# def customize_product_view(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     thumbnails = []
#     for thumb in [product.thumbnail1, product.thumbnail2, product.thumbnail3, product.thumbnail4, product.thumbnail5]:
#         if thumb:
#             thumbnails.append(thumb.url)

#     try:
#         color_variants = json.loads(product.color_options or "[]")
#     except:
#         color_variants = []

#     return render(request, 'customize.html', {
#         'product': product,
#         'thumbnails': thumbnails,
#         'color_variants': color_variants,
#     })
def customize_product_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Get thumbnails
    thumbnails = []
    for thumb in [product.thumbnail1, product.thumbnail2, product.thumbnail3, product.thumbnail4, product.thumbnail5]:
        if thumb:
            thumbnails.append(thumb.url)

    # Get color options
    try:
        color_variants = json.loads(product.color_options or "[]")
    except:
        color_variants = []

    # 🔁 Related products by same category
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    return render(request, 'customize.html', {
        'product': product,
        'thumbnails': thumbnails,
        'color_variants': color_variants,
        'related_products': related_products,  # ✅ pass to template
    })


def cart_view(request):
    return render(request, 'cart.html')
def placeorder_view(request):
    product_id = request.GET.get('product_id')
    quantity = int(request.GET.get('quantity', 1))
    
    product = get_object_or_404(Product, pk=product_id)

    return render(request, 'placeorder.html', {
        'product': product,
        'quantity': quantity,
        'total_price': product.price * quantity,
    })

def add_to_save(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        if product_id:
            product_id = int(product_id)
            # Get the current saved list from session
            saved = request.session.get('recently_viewed', [])

            # Add if not already saved
            if product_id not in saved:
                saved.insert(0, product_id)
                if len(saved) > 10:
                    saved = saved[:10]  # Keep only 10 items
                request.session['recently_viewed'] = saved

    return redirect('save')

def save_view(request):
    saved_ids = request.session.get('recently_viewed', [])
    products = Product.objects.filter(id__in=saved_ids)

    # To preserve order
    products = sorted(products, key=lambda x: saved_ids.index(x.id))

    return render(request, 'save.html', {'products': products})

# def contact_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')

#         subject = f"New Contact Form Submission from {name}"
#         full_message = f"""
#         Name: {name}
#         Email: {email}
#         Phone: {phone}
#         Message: {message}
#         """

#         send_mail(
#             subject,
#             full_message,
#             'your_email@gmail.com',  # From email
#             ['furniflex@gmail.com'],  # To email (or a list of recipients)
#             fail_silently=False,
#         )

#         messages.success(request, 'Your message has been sent successfully!')
#         return redirect('/')  # or render a thank-you page

#     return render(request, 'home.html')
@login_required
def upload_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_image'):
        profile = request.user.userprofile
        profile.profile_image = request.FILES['profile_image']
        profile.save()
    return redirect('account')  


def send_contact_email(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        subject = f"New Contact Form Submission from {name}"
        body = f"""
        Name: {name}
        Email: {email}
        Phone: {phone}
        Message: {message}
        """

        send_mail(
            subject,
            body,
            email,  # from email (sender)
            ['sandhyanepal54@gmail.com'],  # to email (receiver)
            fail_silently=False,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect('home')  # or wherever you want to redirect

    return redirect('home')
@csrf_exempt
def save_payment_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        user = request.user
        product_id = data.get('product_id')
        product = Product.objects.get(id=product_id)

        full_name = data.get('full_name')
        phone = data.get('phone')
        city = data.get('city')
        address = data.get('address')
        token = data.get('token')
        amount = data.get('amount')

        Payment.objects.create(
            user=user,
            product=product,
            full_name=full_name,
            phone=phone,
            city=city,
            address=address,
            khalti_token=token,
            amount=amount / 100  # if amount is in paisa
        )

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'failed'}, status=400)

def search_view(request):
    search_query = request.GET.get('q', '').strip()
    category_name = request.GET.get('type', '').strip()

    categories = Category.objects.all().order_by('name')
    products = Product.objects.all()

    if category_name and category_name.lower() != "all":
        products = products.filter(category__name__iexact=category_name)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    for product in products:
        try:
            product.color_options = json.loads(product.color_options or "[]")
        except:
            product.color_options = []

    return render(request, 'search.html', {
        'products': products,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_name,
    })
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Product, ProductReview
import json

@csrf_exempt
def submit_review(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        rating = data.get('rating')
        product_id = data.get('product_id')

        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'})

        try:
            product = Product.objects.get(id=product_id)
            # Prevent duplicate review per user-product
            existing_review = ProductReview.objects.filter(user=request.user, product=product).first()
            if existing_review:
                existing_review.rating = rating
                existing_review.save()
            else:
                ProductReview.objects.create(
                    user=request.user,
                    product=product,
                    rating=rating
                )

            # Optionally, update product rating average
            all_reviews = ProductReview.objects.filter(product=product)
            avg_rating = sum(r.rating for r in all_reviews) / all_reviews.count()
            product.rating = round(avg_rating, 1)
            product.reviews = all_reviews.count()
            product.save()

            return JsonResponse({'status': 'success'})

        except Product.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Product not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
