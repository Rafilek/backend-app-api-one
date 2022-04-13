from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='elmito@elmi.pl', password='elmitoPasssword'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is succesful"""
        email = 'testuser@hotmail.com'
        password = 'TestP@$$word'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'testuser@HOTMAIL.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """ Test creating user with no email raises error """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, '123')

    def test_create_new_superuser(self):
        """Testing creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test"hotmail.com',
            '123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Not Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredients_str(self):
        """Test that the ingredient exists"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Papaya'
        )

        self.assertEqual(str(ingredient), ingredient.name)
