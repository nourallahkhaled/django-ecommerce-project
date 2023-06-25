from django.shortcuts import render, get_object_or_404
from . models import *
from rest_framework.response import Response
from . serializer import *
from rest_framework.decorators import api_view
from rest_framework import status

# ----------- CUSTOMERS API -------------
@api_view(['GET'])
def get_all_customers_api(request):
    data = {}
    try:
        customers = Customer.objects.all()
        customers_serializer = CustomerSerializer(customers, many=True)
        data = customers_serializer.data
        http_status = status.HTTP_200_OK
    except Exception as e:
        print(f'exception in get_all_customers_api => {e}')
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=http_status)

@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, id):
    data = {}
    try:
        customer = get_object_or_404(Customer, id=id)
        if request.method == 'GET':
            customer_serializer = CustomerSerializer(instance=customer)
            data = customer_serializer.data
            http_status = status.HTTP_200_OK
        if request.method == 'PUT':
            customer_serializer = CustomerSerializer(instance=customer, data=request.data, partial=True)
            if customer_serializer.is_valid():
                customer_serializer.save()
                data = customer_serializer.data
                http_status = status.HTTP_200_OK
        if request.method == 'DELETE':
            customer.delete()
            http_status = status.HTTP_204_NO_CONTENT
    except Exception as e:
        print(f'exception in one customer => {e}')
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=http_status)

# ---------- PRODUCTS API ----------------
@api_view(['GET', 'POST'])
def product_list(request):
    data = {}
    try:
        if request.method == 'GET':
            # Check if a search query is provided
            search_query = request.query_params.get('search', None)
            if search_query:
                products = Product.objects.filter(productName__icontains=search_query)
            else:
                products = Product.objects.all()
            products_serializer = ProductSerializer(products, many=True)
            data = products_serializer.data
            http_status = status.HTTP_200_OK
        elif request.method == 'POST':
            product_serializer = ProductSerializer(data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                data = product_serializer.data
                http_status = status.HTTP_201_CREATED
            else:
                data = product_serializer.errors
                http_status = status.HTTP_400_BAD_REQUEST
    except Exception as e:
        print(f'exception in product_list => {e}')
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=http_status)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, id):
    data = {}
    try:
        product = get_object_or_404(Product, id=id)
        if request.method == 'GET':
            product_serializer = ProductSerializer(instance=product)
            data = product_serializer.data
            http_status = status.HTTP_200_OK
        if request.method == 'PUT':
            product_serializer = ProductSerializer(instance=product, data=request.data, partial=True)
            if product_serializer.is_valid():
                product_serializer.save()
                data = product_serializer.data
                http_status = status.HTTP_200_OK
            else:
                data = product_serializer.errors
                http_status = status.HTTP_400_BAD_REQUEST
        if request.method == 'DELETE':
            product.delete()
            http_status = status.HTTP_204_NO_CONTENT
    except Exception as e:
        print(f'exception in product_detail => {e}')
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=http_status)

# ========= Login & Registeration =========
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# @api_view(['POST'])
# def login_view(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             login(request, user)
#             return JsonResponse({'success': True})
#         else:
#             return JsonResponse({'success': False, 'error': 'Invalid username or password.'})
#     else:
#         return JsonResponse({'success': False, 'error': 'Invalid request method.'})

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializer import CartItemSerializer
from .permissions import IsCartOwner

class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ======= Register ========
@api_view(['POST'])
@csrf_exempt
def add_customer_api(request):
    data = {}
    try:
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            # create a new user object
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.create_user(email, password=password)
            user.save()

            # create a new customer object and set the user field
            customer = serializer.save(user=user)
            data = serializer.data
            http_status = status.HTTP_201_CREATED
            login(request, user)
        else:
            data = serializer.errors
            http_status = status.HTTP_400_BAD_REQUEST
    except Exception as e:
        print(f'exception in create api => {e}')
        data = {'error': 'An error occurred.'}
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=http_status)

# ======= Login ========
@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # create a Customer object for the authenticated user
            customer, created = Customer.objects.get_or_create(user=user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})
    
def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})


from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Product
from .serializer import CartItemSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += quantity
    cart_item.save()
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_cart(request):
    item_id = request.data.get('item_id')
    quantity = request.data.get('quantity')
    if quantity is None or not quantity.isdigit():
        return Response({'detail': 'Invalid quantity'}, status=400)
    quantity = int(quantity)
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user.customer)
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
    else:
        cart_item.delete()
    return Response(status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    item_id = request.data.get('item_id')
    cart_item = get_object_or_404(CartItem, id=item_id, cart__customer=request.user.customer)
    cart_item.delete()
    return Response(status=204)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart(request):
    cart, created = Cart.objects.get_or_create(customer=request.user.customer)
    cart_items = cart.cartitem_set.all()
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data)

