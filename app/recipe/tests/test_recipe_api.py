from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Recipe, Tag, Ingredient
from recipe.serializers import RecipeDetailSerializer, RecipeSerializer

RECIPES_URL = reverse('recipe:recipe-list')


class PublicRecipeApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required in order to access this endpoint"""
        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@elmi.pl',
            'password123'
        )

        self.client = APIClient()

        self.client.force_authenticate(self.user)

    def detail_url(recipe_id):
        """Return recipe detail url """
        return reverse('recipe:recipe-detail', args=[recipe_id])

    def sample_tag(user, name='Main course'):
        """Create and returna a sample tag to test"""
        return Tag.objects.create(user=user, name=name)

    def sample_ingredient(user, name='Cinamon'):
        """Create and return a sample ingredient"""
        return Ingredient.objects.create(user=user, name=name)

    def sample_recipe(user, **params):
        """Test create a basic recipe"""
        payload = {
            'title': 'El mejor batido de melon del mundo.',
            'price': 3.78,
            'time_minutes': 2
        }

        payload.update(params)

        return Recipe.objects.create(user=user, **payload)

    def test_view_recipe_detail(self):
        """Test that we can view the details of recipe"""

        recipe = sample_recipe(user=self.user)
        recipe.tags.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredient(user=self.user))

        url = detail_url(recipe.id)
        res = self.client.get(url)

        serializer = RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
