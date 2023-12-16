from rest_framework import serializers

from order.models import PurchaseOrder
from vendor.models import HistoricalPerformance


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status',
                  'quality_rating',)
        read_only_fields = ('vendor', 'po_number')

        extra_kwargs = {
            'items': {'required': True, },
            'delivery_date': {'required': True},
            'quantity': {'required': True},
            'status': {'required': True},
            'quality_rating': {'required': True},
        }

    def create(self, validated_data):
        # Generate a unique po_number (you may customize this logic based on your requirements)
        po_number = PurchaseOrder.objects.count() + 1
        validated_data['po_number'] = f'PO-{po_number}'

        return super().create(validated_data)


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ('id', 'po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status',
                  'quality_rating', 'issue_date', 'acknowledgment_date',)


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = ['id', 'vendor', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time',
                  'fulfillment_rate']


class AcknowledgeSerializer(serializers.Serializer):
    acknowledgment_date = serializers.DateTimeField()
