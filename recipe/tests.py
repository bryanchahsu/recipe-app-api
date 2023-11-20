"""
Tests for recipe APIs.
"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Recipe, Inventory
from recipe.serializers import (
    RecipeSerializer,
    RecipeDetailSerializer,
    ProductSerializer,
    ProductDetailSerializer
)
# RECIPES_URL = reverse('try:recipe-list')
RECIPES_URL = reverse('recipe-list')
PRODUCTS_URL = reverse('product-list')


def detail_url(recipe_id):         
    """Create and return a recipe detail URL."""
    return reverse('recipe:recipe-detail', args=[recipe_id])

def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults = {
        'title': 'Sample recipe title',
        'time_minutes': 22,
        'price': Decimal('5.25'),
        'description': 'Sample description',
        'link': 'http://example.com/recipe.pdf',
    }
    defaults.update(params)
    recipe = Recipe.objects.create(user=user, **defaults)
    return recipe

# RECIPES_URL_2 = reverse('product')
# PRODUCTS_URL= "http://localhost:8000/api/recipe/productlist/"
# RECIPES_URL = reverse('recipe:recipe-list')


# class PracticeAPITests(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
    
#     def test_auti(self):
#         res = self.client.get(PRODUCTS_URL)
#         self.assertEqual(res.status_code, 401)



#Test authentication that the server auth. works against public users
# class PublicProductAPITests(TestCase):
#     def setUp(self) -> None:
#         self.client = APIClient()
#     def test_auth_required(self):
#         res = self.client.get(PRODUCTS_URL)
#         self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateProductAPITests(TestCase):
    #test for ingredient 
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    
    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes"""
        # create_recipe(user=self.user)
        # create_recipe(user=self.user)
        res = self.client.get(PRODUCTS_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_productdetail(self):
        pass


    def test_create_recipe_Notingred(self):
        #test if django can use api to create a recipe with an """nonexistent""" ingredient
        pass
        
    
    def test_create_recipe_ingred(self):
        #test if django can use api to create a recipe with an """existent""" ingredient
        pass

    def test_patch_notexist(self):
        """!!!!!!!!!!!!!! 1. IMPORTANT Note: YOU SHOULD NOT CREATE AN NON-EXISTENT INGREDIENT WHILE PATCHING A RECIPE
                          2. NEED ERROR HANDLING?"""
        """test if you can create a ingredient while patching a recipe"""
        pass



    def test_patch_exist(self):
        """test if you can patch a ingredient with an existing recipe"""
        pass



class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()
    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(RECIPES_URL)
        # self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeApiTests(TestCase):
    """Test authenticated API requests."""
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        # create_recipe(user=self.user)
        # create_recipe(user=self.user)
        # res = self.client.get(RECIPES_URL)
        res = self.client.get(PRODUCTS_URL)
        # recipes = Recipe.objects.all().order_by('-id')
        # serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    def test_recipe_list_limited_to_user(self):
        """Test list of recipes is limited to authenticated user."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_recipe(user=other_user)
        create_recipe(user=self.user)
        res = self.client.get(RECIPES_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    # def test_get_recipe_detail(self):
    #     """Test get recipe detail."""
    #     recipe = create_recipe(user=self.user)
    #     url = detail_url(recipe.id)
    #     res = self.client.get(url)

    #     serializer = RecipeDetailSerializer(recipe)
    #     self.assertEqual(res.data, serializer.data)

    def test_create_recipe(self):
        """Test creating a recipe."""
        payload = {
            'title': 'Sample recipe',
            'time_minutes': 30,
            'price': Decimal('5.99'),
        }
        # res = self.client.post(RECIPES_URL, payload)

        # self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # recipe = Recipe.objects.get(id=res.data['id'])
        # for k, v in payload.items():
        #     self.assertEqual(getattr(recipe, k), v)
        # self.assertEqual(recipe.user, self.user)
