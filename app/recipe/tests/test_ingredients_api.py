from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient
from recipe.serializers import IngredientSerializer


INGREDIENT_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that the login is required to access this endpoint"""
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password123'
        )

        self.client = APIClient()

        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients_list(self):
        """Test retrieve ingredients"""
        Ingredient.objects.create(user=self.user, name='Oil')
        Ingredient.objects.create(user=self.user, name='Mint')

        res = self.client.get(INGREDIENT_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_for_user(self):
        """Test that only ingredients for authenticated users are returned"""
        user2 = get_user_model().objects.create_user(
            'other@elmi.pl',
            'otherPassw0rd'
        )
        Ingredient.objects.create(user=user2, name='Lettuce')
        ingredient = Ingredient.objects.create(user=self.user, name='Tomato')

        res = self.client.get(INGREDIENT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)

    def test_create_ingredient_succesful(self):
        """ Test create a new ingredient """
        payload = {'name': 'Soup'}
        self.client.post(INGREDIENT_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_invalid_ingredient(self):
        """ Test create an invalid ingredient"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENT_URL, payload)

        self.assertTrue(res.status_code, status.HTTP_400_BAD_REQUEST)
