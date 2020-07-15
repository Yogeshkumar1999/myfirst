from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null = True, blank=True, on_delete= models.CASCADE)

    name = models.CharField(max_length = 200, null = True)
    phone = models.CharField(max_length = 20, null = True)
    email = models.CharField(max_length = 200, null = True)
    profile_pic = models.ImageField(null = True, blank = True, default = 'logo.png')
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.name

#To get the manay to many relationship we are creating the tag class
#so product and tag many ti many relationship.

class Tag(models.Model):
    name = models.CharField(max_length = 200, null = True)
    #date_created = models.DateTimeField(auto_now_add = True, null = True)
    def __str__(self):
        return self.name


class Product(models.Model):
    #to get the dropdown for the category need to give tuple of tuple.

    CATEGORY = (
                ('Indoor', 'Indoor'),
                ('Outdoor', 'Outdoor'),
            )

    name = models.CharField(max_length = 200, null = True)
    category = models.CharField(max_length = 200, null = True, choices = CATEGORY)
    price = models.FloatField(null = True)
    description = models.CharField(max_length = 255, null = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Order(models.Model):
    #To get the dropdown in status filed.
    STATUS = (
                ('Pending', 'Pending'),
                ('Out for delivery', 'Out for delivery'),
                ('Delivered', 'Delivered'),
            )
    customer = models.ForeignKey(Customer, null = True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null = True, on_delete = models.SET_NULL)
    status = models.CharField(max_length = 100, null = True, choices=STATUS, default = 'Pending')
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    def __str__(self):
        return self.product.name

