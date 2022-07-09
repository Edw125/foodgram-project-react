import base64
from http import HTTPStatus

from rest_framework.test import APIClient, APITestCase

from recipes.models import IngredientAmount, Recipe, Ingredient, Tag
from users.models import User, Follow

SMALL_GIF = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)


class UserModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="user",
            email="user@example.com",
            first_name="Иван",
            last_name="Иванов",
            is_active=True,
            is_staff=False,
            is_admin=False,
        )
        cls.author = User.objects.create_user(
            username="author",
            email="author@example.com",
            first_name="Алексей",
            last_name="Алексеев",
            is_active=True,
            is_staff=False,
            is_admin=False,
        )
        cls.follow = Follow.objects.create(
            user=cls.user, author=cls.author,
        )
        cls.tag = Tag.objects.create(
            name='tag', hex_color="#ffffff", slug="tag"
        )
        cls.ingredient = Ingredient.objects.create(
            name="product", measurement_unit="kg"
        )
        cls.recipe = Recipe.objects.create(
            author=cls.author,
            name="Recipe",
            image=f"data:image/png;base64,"
                  f"{base64.b64encode(SMALL_GIF).decode('utf-8')}",
            text="Description",
            cooking_time=60
        )
        cls.recipe.tags.set([cls.tag])
        cls.ingredient_amount = IngredientAmount.objects.create(
            recipe=cls.recipe, ingredient=cls.ingredient, amount=60)
        cls.recipe.ingredients.set([cls.ingredient])

    def setUp(self):
        self.guest_client = APIClient()
        self.authorized_client = APIClient()
        self.authorized_client.force_authenticate(user=self.user)

    def test_user_model(self):
        """Проверяем поля модели user."""
        self.assertIsInstance(self.user.username, str)
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)
        self.assertIsInstance(self.user.is_active, bool)
        self.assertIsInstance(self.user.is_admin, bool)
        self.assertIsInstance(self.user.is_staff, bool)

    def test_follow_model(self):
        """Проверяем поля модели follow."""
        self.assertIsInstance(self.follow.user, User)
        self.assertIsInstance(self.follow.author, User)

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        user = UserModelTest.user
        self.assertEqual(user.__str__(), self.user.email)

    def test_url_user_subscriptions(self):
        """Проверка доступа к эндпоинту subscriptions."""
        response = self.authorized_client.get(
            '/api/users/subscriptions/'
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
