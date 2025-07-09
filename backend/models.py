from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    thumbnail1 = models.ImageField(upload_to='products/', blank=True, null=True)
    thumbnail2 = models.ImageField(upload_to='products/', blank=True, null=True)
    thumbnail3 = models.ImageField(upload_to='products/', blank=True, null=True)
    thumbnail4 = models.ImageField(upload_to='products/', blank=True, null=True)
    thumbnail5 = models.ImageField(upload_to='products/', blank=True, null=True)
    color_options = models.JSONField(default=list)  # e.g. ["black", "gray"]
    reviews = models.PositiveIntegerField(default=0)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    profile_image = models.ImageField(upload_to='profile_images/', default='profile_images/default.jpg')

    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.TextField()
    khalti_token = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.user.username} for {self.product.name}"
