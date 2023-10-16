from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.response import Response

from .models import Order, OrderAttachment
from .permissions import CanCreateOrderPermission, CanRetrieveOrderPermission
from .serializers import OrderSerializer, OrderAttachmentSerializer


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CanCreateOrderPermission]

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()


class OrderAttachmentCreateView(generics.CreateAPIView):
    queryset = OrderAttachment.objects.all()
    serializer_class = OrderAttachmentSerializer

    def perform_create(self, serializer):
        order = get_object_or_404(Order, pk=self.kwargs['order_pk'])
        serializer.save(order=order)

    def handle_exception(self, exc):
        # Обработать исключение, если заказ не найден
        if isinstance(exc, Http404):
            return Response({"detail": "Order not found."},
                            status=status.HTTP_404_NOT_FOUND)

        # Для всех других исключений вызвать родительскую реализацию
        return super().handle_exception(exc)


class OrderRetrieveView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [CanRetrieveOrderPermission]
    lookup_field = 'order_number'
