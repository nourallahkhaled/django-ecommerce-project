from django.shortcuts import render
from rest_framework.views import APIView
from . models import *
from rest_framework.response import Response
from . serializer import *
# Create your views here.

class ReactView(APIView):
    
    serializer_class = ProductSerializer

    def get(self, request):
        output = [{"productName": output.productName, "productDescription": output.productDescription,"productQuantity": output.productQuantity, "productPrice": output.productPrice}
                  for output in Product.objects.all()]
        return Response(output)

    def post(self, request):

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)