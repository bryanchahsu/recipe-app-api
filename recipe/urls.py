"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views


router = DefaultRouter()
# router.register('recipes', views.RecipeViewSet)
# router.register('recipes', views.ProductList)

router.register('recipes', views.RecipeViewSet, basename= 'recipe' )
router.register('products', views.ProductViewSet, basename= 'product' )

# app_name = 'recipe'
# app_name = 'try'

urlpatterns = [
    # path('products',views.ProductList.as_view({'get':'list'}),name='product'),
    # path('', include((router.urls,'product'), namespace='product'))
    path('', include(router.urls))
    # path('products/', views.ProductList.as_view({'get':'list'}), name = 'product-list')
    # path('blogs', include(router.urls)),
    # path('blogs/', views.ProductList.as_view(), name='test')

]