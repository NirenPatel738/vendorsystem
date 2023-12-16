from django.urls import path

from order import views

urlpatterns = [
    path('purchase_order/', views.PurchaseOrderCreateView.as_view(), name='purchase_order_create'),
    path('purchase_order_list/', views.PurchaseOrderListView.as_view(), name='purchase_order_list'),
    path('purchase_order_retrieve/<int:pk>/', views.PurchaseOrderRetrieveView.as_view(), name='purchase_order_retrieve'),
    path('purchase_order_update/<int:pk>/', views.PurchaseOrderUpdateView.as_view(), name='purchase_order_update'),
    path('purchase_order_delete/<int:pk>/', views.PurchaseOrderDeleteView.as_view(), name='purchase_order_delete'),
    path('purchase_orders/<int:po_id>/acknowledge/', views.acknowledge_purchase_order, name='acknowledge_purchase_order'),
    path('vendors/<int:vendor_id>/performance/', views.VendorPerformanceView.as_view(), name='vendor-performance'),
]