from rest_framework import serializers
from . models import *
from rest_framework import serializers
from .models import Customer, Product, Order, OrderItem, Address, Cart, CartItem

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'email', 'firstName', 'lastName','password']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'productName', 'productDescription', 'productQuantity', 'productPrice']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'date_orderd', 'complete', 'transaction_id', 'order_items']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'customer', 'order', 'address', 'governorate', 'city', 'date_added', 'default']


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='pk')
    product = serializers.CharField(source='product.productName')
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, obj):
        return obj.product.productPrice * obj.quantity

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'customer', 'date_added', 'cart_items']

# class WishlistSerializer(serializers.ModelSerializer):
#     wishlist_items = ProductSerializer(many=True)

#     class Meta:
#         model = Wishlist
#         fields = ['id', 'customer', 'date_added', 'wishlist_items']