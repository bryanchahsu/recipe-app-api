from django.shortcuts import render
"""
Views for the recipe APIs
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

# Create your views here.
from core.models import Recipe, Inventory, Product
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
        # return self.queryset



    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

################ TEST (PASS) #############################


# class ProductList(viewsets.ModelViewSet):
#     """View for manage recipe APIs."""
    # serializer_class = serializers.RecipeSerializer
    # queryset = Recipe.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     """Retrieve recipes for authenticated user."""
    #     return self.queryset.filter(user=self.request.user).order_by('-id')
##################################################################


################ TEST (DO NOT USE) #############################


class ProductViewSet(viewsets.ModelViewSet):

    """View for manage recipe APIs."""
    # serializer_class = serializers.RecipeSerializer
    serializer_class = serializers.ProductSerializer
    queryset = Product.objects.all() 
    
    #ERASED AUTHENTICATION => empty the brackets
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        # return self.queryset
        return self.queryset.filter(user=self.request.user).order_by('-id')

        """Determine if the request is list or detail"""
    def get_serializer_class(self):

        if self.action == 'list':
            return serializers.ProductSerializer
        
        return self.serializer_class
    

    def perform_create(self, serializer):
        return serializer.save()
