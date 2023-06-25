from django.shortcuts import render

# Create your views here.
from rest_framework import generics,permissions
from .models import Wishlist
from .serializers import WishlistSerializer



# class wishList(generics.ListAPIView):
#     serializer_class = WishlistSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def get_queryset(self):
#         user_id = self.kwargs['user_id']
#         queryset = Wishlist.objects.filter(user_id=user_id)
#         return queryset

class wishList(generics.ListCreateAPIView):
    serializer_class = WishlistSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Wishlist.objects.filter(user_id=user_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Set the user on the newly created object

class WishListDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer

