from django.urls import path
from .views import ProductInventoryView, ProductDetailView, ProductDeleteView, ProductUpdateView, ProductCreateView



urlpatterns = [
    path('', ProductInventoryView.as_view(), name='product-list'),
    # path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>', ProductDetailView.as_view(), name='product-detail'),

    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product-update'),
    path('new', ProductCreateView.as_view(), name='product-create'),



]