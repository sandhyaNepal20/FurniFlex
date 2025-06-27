"""
URL configuration for FurniFlex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views  # ✅ This line fixes the error

from FurniFlex.views import home_view
from .views import logout_view, home_view

urlpatterns = [
    path('admin/', admin.site.urls),
        path('', home_view, name='home') , # Use 'home' as the name for the root URL
        path('cart/', views.cart_view, name='cart'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('reset-password/', views.password_reset_view, name='password_reset'),
    path('searchproduct/', views.search_product_view, name='searchproduct'),
        path('account/', views.account_view, name='account'),
            path('edit-profile/', views.edit_profile_view, name='editprofile'),
                path('category/', views.category_view, name='category'),
                    path('customize/', views.customize_view, name='customize'),
                    path('cart/', views.cart_view, name='cart'),
                        path('logout/', logout_view, name='logout'),
                            path('placeorder/', views.placeorder_view, name='placeorder'),












]
