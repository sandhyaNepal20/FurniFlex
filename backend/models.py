from django.db import models
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

    def __str__(self):
        return self.user.first_name