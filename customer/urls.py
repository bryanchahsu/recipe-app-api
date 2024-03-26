from django.urls import path
from .views import CustomerListView, CustomerDetailView, CustomerUpdateView, CustomerDeleteView, CustomerCreateAPIView



urlpatterns = [
    path('', CustomerListView.as_view(), name='customer-list'),
    path('<int:customer_id>/', CustomerDetailView.as_view(), name='customer-detail'),
    path('customers/<int:customer_id>/update/', CustomerUpdateView.as_view(), name='customer-update'),
    path('new', CustomerCreateAPIView.as_view(), name='customer-create'),
    path('customer/<int:pk>/delete/', CustomerDeleteView.as_view(), name='customer-delete')





]