from django.urls import path
from vendor.views import Register, LoginAPI, ChangePasswordView, UpdateProfileView, VendorView, VendorListView, \
	LogoutAPIView, VendorDeleteAPIView

urlpatterns = [

	path('register/', Register.as_view()),
	path('login/', LoginAPI.as_view()),
	path('logout/', LogoutAPIView.as_view()),
	path('change_password/<int:pk>/', ChangePasswordView.as_view()),
	path('vendor_profile/', VendorView.as_view()),
	path('vendors_list/', VendorListView.as_view()),
	path('update_profile/<int:pk>/', UpdateProfileView.as_view()),
	path('vendor_delete/<int:pk>/', VendorDeleteAPIView.as_view(), name='vendor-delete'),

]