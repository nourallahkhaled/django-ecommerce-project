from django.shortcuts import render, get_object_or_404
from . models import *
from rest_framework.response import Response
from . serializer import *
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.
# class ReactView(APIView):
#     serializer_class = ProductSerializer
#     def get(self, request):
#         output = [{"productName": output.productName, "productDescription": output.productDescription,"productQuantity": output.productQuantity, "productPrice": output.productPrice}
#                   for output in Product.objects.all()]
#         return Response(output)
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)

# class CustomerListView(APIView):
#     def get(self, request):
#         customers = Customer.objects.all()
#         serializer = CustomerSerializer(customers, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)


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
@api_view(['GET'])
def get_all_products_api(request):
    data = {}
    try:
        products = Product.objects.all()
        products_serializer = ProductSerializer(products, many=True)
        data = products_serializer.data
        http_status = status.HTTP_200_OK
    except Exception as e:
        print(f'exception in get_all_products_api => {e}')
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
        if request.method == 'DELETE':
            product.delete()
            http_status = status.HTTP_204_NO_CONTENT
    except Exception as e:
        print(f'exception in one product => {e}')
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=http_status)


# ========= Login & Registeration =========
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid username or password.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})
    
    

def logout_view(request):
    logout(request)
    return JsonResponse({'success': True})


@api_view(['POST'])
@csrf_exempt
def add_customer_api(request):
    data = {}
    try:
        customers = CustomerSerializer(data=request.data)
        if customers.is_valid():
            customer = customers.save()
            data = customers.data
            http_status = status.HTTP_201_CREATED
            user = User.objects.create_user(customer.email, password=customer.password)
            user.save()
            login(request, user)
        else:
            data = customers.errors
            http_status = status.HTTP_400_BAD_REQUEST
    except Exception as e:
        print(f'exception in create api => {e}')
        data = {'error': 'An error occurred.'}
        http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(data=data, status=http_status)