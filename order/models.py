from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models import Avg, F

# from vendor.models import Vendor
from vendor.models import HistoricalPerformance

UserModel = get_user_model()


class PurchaseOrder(TimeStampedModel):
    ORDER_STATUS = Choices(
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )
    po_number = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="vendor_order")
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=250, choices=ORDER_STATUS, default=ORDER_STATUS.pending)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Purchase Order')
        verbose_name_plural = _('Purchase Orders')

    def __str__(self):
        return self.po_number

    @property
    def is_completed(self):
        return self.status == PurchaseOrder.ORDER_STATUS.completed


@receiver(post_save, sender=PurchaseOrder)
def calculate_metrics(sender, instance, created, **kwargs):
    if instance.is_completed:
        # On-Time Delivery Rate
        completed_orders = PurchaseOrder.objects.filter(vendor=instance.vendor,
                                                        status=PurchaseOrder.ORDER_STATUS.completed)

        on_time_deliveries = completed_orders.filter(delivery_date__lte=F('acknowledgment_date'))
        total_completed_purchases = completed_orders.count()

        # Calculate On-Time Delivery Rate
        on_time_delivery_rate = (
            on_time_deliveries.count() / total_completed_purchases
            if total_completed_purchases > 0
            else 0
        )

        # Quality Rating Average
        quality_ratings = PurchaseOrder.objects.filter(vendor=instance.vendor,
                                                       status=PurchaseOrder.ORDER_STATUS.completed,
                                                       quality_rating__isnull=False)
        quality_rating_avg = quality_ratings.aggregate(avg_quality_rating=Avg('quality_rating'))['avg_quality_rating']

        # Average Response Time
        response_times = PurchaseOrder.objects.filter(vendor=instance.vendor,
                                                      acknowledgment_date__isnull=False).exclude(
            issue_date__isnull=True)
        avg_response_time = response_times.aggregate(avg_response_time=Avg(F('acknowledgment_date') - F('issue_date')))[
            'avg_response_time']

        # Convert timedelta to total seconds
        # avg_response_time_seconds = avg_response_time.total_seconds()

        # Check if avg_response_time is not None before accessing total_seconds()
        avg_response_time_seconds = (
            avg_response_time.total_seconds() if avg_response_time is not None else None
        )
        # Fulfilment Rate
        successful_fulfillments = completed_orders.exclude(quality_rating__lt=0)
        fulfillment_rate = successful_fulfillments.count() / PurchaseOrder.objects.filter(
            vendor=instance.vendor).count()

        # Update HistoricalPerformance
        historical_performance, created = HistoricalPerformance.objects.get_or_create(vendor=instance.vendor)
        historical_performance.on_time_delivery_rate = on_time_delivery_rate
        historical_performance.quality_rating_avg = quality_rating_avg
        historical_performance.average_response_time = avg_response_time_seconds
        historical_performance.fulfillment_rate = fulfillment_rate
        historical_performance.save()
