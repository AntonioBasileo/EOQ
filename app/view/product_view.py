from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.dto.dto import ProductReadSerializer, ProductWriteSerializer
from app.model.eoq_models import Product
from django.shortcuts import get_object_or_404

from app.permissions.permissions import ProductPermissions


class ProductView(APIView):

    permission_classes = [ProductPermissions]

    @staticmethod
    def get(request, pk: int):
        product = get_object_or_404(Product, pk=pk)

        return Response(ProductReadSerializer(product).data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        serializer = ProductWriteSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductReadSerializer(product).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductAllListView(APIView):
    permission_classes = [ProductPermissions]

    @staticmethod
    def get(request):
        serializer = ProductReadSerializer(Product.objects.all(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductDetailView(APIView):

    permission_classes = [ProductPermissions]

    @staticmethod
    def put(request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductWriteSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            product = serializer.save()

            return Response(ProductReadSerializer(product).data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, pk):
        get_object_or_404(Product, pk=pk).delete()

        return Response(status=status.HTTP_200_OK)
