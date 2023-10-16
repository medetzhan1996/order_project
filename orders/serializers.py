from rest_framework import serializers
from .models import Order, OrderAttachment


class OrderAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderAttachment
        fields = ['file']


class OrderSerializer(serializers.ModelSerializer):
    attachments = OrderAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'site_type', 'description', 'budget',
                  'deadline', 'attachments', 'order_number']
