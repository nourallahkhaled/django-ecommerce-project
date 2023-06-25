from django.urls import path

from .views import wishList , WishListDetailView

urlpatterns = [
    
    path('<int:user_id>/', wishList.as_view()),
    path('wishlist/<int:pk>/', WishListDetailView.as_view()),
]