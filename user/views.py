"""
Views for the user API.
"""
from rest_framework import generics
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
# Return product list
# 


#### Algorithm ####

#1. create api as view
#2. update url path with the correct view (import)
# class ProductList(viewsets.ModelViewSet):
# class ProductList(generics.CreateAPIView):
#     serializer_class = ProductSerializer
    
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]

#     def get_queryset():
#         # return self.queryset.filter(user=self.request.user).order_by('-id')
#         queryset = Inventory.objects.all()
#         return queryset
