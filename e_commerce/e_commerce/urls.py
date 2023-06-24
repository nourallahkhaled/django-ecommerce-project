"""
URL configuration for e_commerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# from wearstore.views import CustomerListView
from wearstore import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/customer/<int:id>', views.customer_detail, name="customer_api"),
    path('api/allcustomers', views.get_all_customers_api, name="all_customers_api"),
    path('api/product/<int:id>', views.product_detail, name="product_api"),
    path('api/allproducts', views.get_all_products_api, name="all_products_api"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registercustomer/', views.add_customer_api, name='redistercustomer'),
    # path('myview/', views.myview, name='myview'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
]

