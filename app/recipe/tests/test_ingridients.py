"""
Tests for the ingredients API.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingridient

from recipe.serializers import IngridientSerializer


INGRIDIENTS_URL = reverse('recipe:ingridient-list')

def detail_url(ingridient_id):
    """Create and return an ingridient detail url"""
    return reverse('recipe:ingridient-detail',args = [ingridient_id])

def create_user(email = 'user@example.com', password = 'testpass123'):
    """Create and return and email"""
    return get_user_model().objects.create_user(
        email = email,
        password = password,
    )

class PublicIngredientsApiTests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()


    def test_auth_required(self):
        """Test auth is required for retrieving an ingridient"""
        res = self.client.get(INGRIDIENTS_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingridients(self):
        """Test retrieving a list of ingredients"""
        Ingridient.objects.create(user=self.user,name = 'Kale')
        Ingridient.objects.create(user=self.user,name = 'Vanila')

        res = self.client.get(INGRIDIENTS_URL)

        ingredients = Ingridient.objects.all().order_by('-name')
        serializer = IngridientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """List of ingredients is limited to authenticated user"""
        user2 = create_user(email = 'user2@example.com')
        Ingridient.objects.create(user=user2,name = 'salt')
        Ingredient = Ingridient.objects.create(user=self.user,name = 'Pepper')

        res = self.client.get(INGRIDIENTS_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],Ingredient.name)
        self.assertEqual(res.data[0]['id'],Ingredient.id)

    def test_update_ingridient(self):
        """Test updating an ingridient"""
        ing = Ingridient.objects.create(user=self.user,name = 'Sugar')
        payload = {'name':'Sugar_updated'}
        url = detail_url(ing.id)
        res = self.client.patch(url,payload)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        ing.refresh_from_db()
        self.assertEqual(ing.name,payload['name'])

    def test_delete_ingridient(self):
        """Test deleting an ingredient."""
        ing = Ingridient.objects.create(user=self.user,name = 'lettuce')
        url = detail_url(ing.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ings = Ingridient.objects.filter(user=self.user)
        self.assertFalse(ings.exists())

