from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.dto.dto import OrderWriteSerializer, OrderReadSerializer
from app.model.eoq_models import Order
from django.shortcuts import get_object_or_404
from app.kafka import producer
from app.permissions.permissions import OrderByUserPermissions, OrderByAdminPermissions
import uuid

class OrderView(APIView):

    permissions = [OrderByUserPermissions]

    @staticmethod
    def get(request, pk: int):
        serializer = OrderReadSerializer(get_object_or_404(Order, pk=pk))

        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        producer.send(str(uuid.uuid4()), request.data)

        return Response("Ordine registrato", status=status.HTTP_200_OK)


class OrderAllListView(APIView):

    permissions = [OrderByAdminPermissions]

    @staticmethod
    def get(request):
        serializer = OrderReadSerializer(Order.objects.all(), many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderByUserView(APIView):

    permissions = [OrderByUserPermissions]

    @staticmethod
    def get(request, username):
        orders = Order.objects.filter(user__username=username)
        serializer = OrderReadSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def delete(request, pk: int):
        get_object_or_404(Order, pk=pk).delete()

        return Response(status=status.HTTP_200_OK)
