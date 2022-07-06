import base64
import os
from http import HTTPStatus

from rest_framework.test import APIClient, APITestCase

from backend.settings import MEDIA_ROOT
from users.models import User
from recipes.models import (Ingredient, IngredientAmount, Recipe,
                            Tag, Favorites, ShoppingCart)

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)


class ApiTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.superuser = User.objects.create_user(
            username="admin", email="admin@example.com",
            first_name="Иван", last_name="Иванов",
            is_active=True, is_staff=True, is_admin=True,
        )
        cls.user = User.objects.create_user(
            username="user", email="user@example.com",
            first_name="Алексей", last_name="Алексеев",
            is_active=True, is_staff=False, is_admin=False,
        )
        cls.tag = Tag.objects.create(
            name='tag', hex_color="#ffffff", slug="tag"
        )
        cls.ingredient = Ingredient.objects.create(
            name="product", measurement_unit="kg"
        )
        cls.recipe = Recipe.objects.create(
            author=cls.user,
            name="Recipe",
            image=f"data:image/png;base64,"
                  f"{base64.b64encode(small_gif).decode('utf-8')}",
            text="Description", cooking_time=60
        )
        cls.recipe.tags.set([cls.tag])
        cls.ingredient_amount = IngredientAmount.objects.create(
            recipe=cls.recipe, ingredient=cls.ingredient, amount=60)
        cls.recipe.ingredients.set([cls.ingredient])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        path = MEDIA_ROOT + '/recipes/'
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)

    def test_unauthorized_url(self):
        """Проверка доступа к эндпоинтам для любых пользователей."""
        url_names = [
            '/api/recipes/',
            '/api/ingredients/',
            '/api/tags/',
            f'/api/recipes/{self.recipe.id}/',
            f'/api/ingredients/{self.ingredient.id}/',
            f'/api/tags/{self.tag.id}/',
        ]

        for address in url_names:
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_recipes(self):
        """Проверка доступа к эндпоинту recipes (post, patch, delete)."""
        data = {"ingredients": [{"id": 1, "amount": 1}],
                "tags": [1],
                "image": f"data:image/png;base64,"
                         f"{base64.b64encode(small_gif).decode('utf-8')}",
                "name": "Recipe",
                "text": "Description",
                "cooking_time": 1
                }
        response = self.authorized_client.post(
            '/api/recipes/', data=data
        )
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        data = {"ingredients": [{"id": 1, "amount": 2}],
                "tags": [1],
                "cooking_time": 2
                }
        response = self.authorized_client.patch(
            f'/api/recipes/{self.recipe.id}/', data=data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.authorized_client.delete(
            f'/api/recipes/{self.recipe.id}/'
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_url_download_shopping_cart(self):
        """Проверка доступа к эндпоинту download_shopping_cart."""
        response = self.authorized_client.get(
            '/api/recipes/download_shopping_cart/'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_shopping_cart(self):
        """Проверка доступа к эндпоинту shopping_cart (post, delete)."""
        response = self.authorized_client.post(
            f'/api/recipes/{self.recipe.id}/shopping_cart/'
        )
        result = ShoppingCart.objects.filter(
            user_id=self.user.id, recipe_id=self.recipe.id
        )
        self.assertTrue(result)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)

        response = self.authorized_client.delete(
            f'/api/recipes/{self.recipe.id}/shopping_cart/'
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)

    def test_url_favorite(self):
        """Проверка доступа к эндпоинту favorite (post, delete)."""
        data = {
            "id": 1,
            "name": "Recipe",
            "image": f"data:image/png;base64,"
                     f"{base64.b64encode(small_gif).decode('utf-8')}",
            "cooking_time": 1
        }
        response = self.authorized_client.post(
            f'/api/recipes/{self.recipe.id}/favorite/', data=data
        )
        result = Favorites.objects.filter(
            user_id=self.user.id, recipe_id=self.recipe.id
        )
        self.assertTrue(result)
        self.assertEqual(response.status_code, HTTPStatus.CREATED)
        response = self.authorized_client.delete(
            f'/api/recipes/{self.recipe.id}/favorite/'
        )
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
