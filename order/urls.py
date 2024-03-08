from django.urls import path
from .views import OrderListView, OrderDetailView, OrderCreateView, OrderUpdateView, OrderDeleteView, OrderListAPIView


urlpatterns = [
    path('', OrderListAPIView.as_view(), name='order-list'),
    # path('', OrderListView.as_view(), name='order-list'),

    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('new', OrderCreateView.as_view(), name='order-create'),
    path('<int:pk>/update/', OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/delete/', OrderDeleteView.as_view(), name='order-delete'),


]
