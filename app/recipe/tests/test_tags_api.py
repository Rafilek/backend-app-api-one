from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from app.recipe.seriliazers import TagSerializer

TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to retrieve tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@gmail.com',
            'password123')

        self.client = APIClient()

        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Poczete obiegi')
        Tag.objects.create(user=self.user, name='Mycie')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.satus_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """TEst that tags returned are for the authenticathed user"""
        user2 = get_user_model().objects.create_user(
            'other@elmi.pl',
            'otherPassw0rd'
        )
        Tag.objects.create(user=self.user, name='Pakowanie')
        tag = Tag.objects.create(user=self.user, name='Wydanie')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
