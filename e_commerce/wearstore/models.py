from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    email = models.EmailField(max_length=255, unique=True,null=False)
    firstName = models.CharField(max_length=30,validators=[
            RegexValidator(
                regex='^[A-Za-z]+$',
                message='Usernames can only contain letters',
                code='invalid_username'
            )
        ],null=False)
    lastName = models.CharField(max_length=30,validators=[
            RegexValidator(
                regex='^[A-Za-z]+$',
                message='Usernames can only contain letters',
                code='invalid_username'
            )
        ],null=False)
    password = models.CharField(max_length=200,validators=[
            RegexValidator(
                regex='^(?=.*[\W]).+$',
                message='Passwords must contain at least one special character',
                code='invalid_password'
            )
        ],null=False)
    # is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.firstName
    
class Product(models.Model):
    productName = models.CharField(max_length=255,null=False)
    #productImage = models.ImageField(upload_to='products/')
    productDescription = models.TextField(null=False)
    productQuantity = models.PositiveIntegerField(null=False)
    productPrice = models.FloatField(null=False)

    def __str__(self):
        return self.productName


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_orderd = models.DateField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.id

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)

class Address(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=200)
    governorate = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.address


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product, through='CartItem')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.productName}'
    
    @property
    def total_price(self):
        return self.product.productPrice * self.quantity
    
# class Wishlist(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     items = models.ManyToManyField(Product, related_name='wishlists')
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return str(self.id)