from django.shortcuts import get_object_or_404
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from utils.permissions import IsAPIKEYAuthenticated
from vendor.models import HistoricalPerformance
from .models import PurchaseOrder, calculate_metrics
from .serializers import PurchaseOrderSerializer, OrderDetailSerializer, HistoricalPerformanceSerializer
from .permissions import IsOrderOwner


class PurchaseOrderCreateView(generics.CreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]

    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)


class PurchaseOrderListView(generics.ListAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated, IsAPIKEYAuthenticated]
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    ordering = ('-created',)

    def get_queryset(self):
        return PurchaseOrder.objects.filter(vendor=self.request.user)


class PurchaseOrderRetrieveView(generics.RetrieveAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner, IsAPIKEYAuthenticated]


class PurchaseOrderUpdateView(generics.UpdateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner, IsAPIKEYAuthenticated]


class PurchaseOrderDeleteView(generics.DestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated, IsOrderOwner, IsAPIKEYAuthenticated]


class VendorPerformanceView(generics.RetrieveAPIView):
    serializer_class = HistoricalPerformanceSerializer
    permission_classes = [IsAPIKEYAuthenticated]

    def get_object(self):
        vendor_id = self.kwargs['vendor_id']
            # Assuming you have a ForeignKey from HistoricalPerformance to User as 'user'
        historical_performance = get_object_or_404(HistoricalPerformance, vendor__id=vendor_id, vendor=self.request.user)
        return historical_performance

    def get(self, request, *args, **kwargs):
        if kwargs['vendor_id'] != self.request.user.id:
            return Response({"error": "Invalid vendor id"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)


@api_view(['POST'])
def acknowledge_purchase_order(request, po_id):
    purchase_order = get_object_or_404(PurchaseOrder, id=po_id)

    # Check if the Purchase Order is pending or accepted
    # if purchase_order.status not in [PurchaseOrder.ORDER_STATUS.pending, PurchaseOrder.ORDER_STATUS.accepted]:
    #     return Response({'error': 'Cannot acknowledge a completed or canceled purchase order.'},
    #                     status=status.HTTP_400_BAD_REQUEST)

    # Update acknowledgment_date
    purchase_order.acknowledgment_date = timezone.now()
    purchase_order.save()

    # Trigger recalculation of average_response_time
    calculate_metrics(sender=PurchaseOrder, instance=purchase_order, created=False)

    return Response({'message': 'Purchase Order acknowledged successfully.'}, status=status.HTTP_200_OK)
