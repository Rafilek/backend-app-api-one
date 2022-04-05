from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from app.core.models import Tag

from app.recipe.seriliazers import TagSerializer


