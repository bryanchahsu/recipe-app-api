"""
Serializers for recipe APIs
"""
from rest_framework import serializers
from core.models import Recipe, Inventory, Product
class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']




class ProductSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""

    class Meta:
        model = Product
        fields = ["names", "description", "quantity"]
        read_only_fields = ['id']


class ProductDetailSerializer(ProductSerializer):
    """Serializer for product detail"""
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['description']
