import base64
import os

from django.test import TestCase

from foodgram.settings import MEDIA_ROOT
from recipes.models import Tag, Ingredient, Recipe, IngredientAmount
from users.models import User

small_gif = (
    b'\x47\x49\x46\x38\x39\x61\x02\x00'
    b'\x01\x00\x80\x00\x00\x00\x00\x00'
    b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
    b'\x00\x00\x00\x2C\x00\x00\x00\x00'
    b'\x02\x00\x01\x00\x00\x02\x02\x0C'
    b'\x0A\x00\x3B'
)


class ModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
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
            recipe=cls.recipe, ingredient=cls.ingredient, amount=60
        )
        cls.recipe.ingredients.set([cls.ingredient])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        path = MEDIA_ROOT + '/recipes/'
        for file in os.listdir(path):
            os.remove(os.path.join(path, file))

    def test_tag_model(self):
        """Проверяем поля модели tag."""
        self.assertIsInstance(self.tag.name, str)
        self.assertIsInstance(self.tag.hex_color, str)
        self.assertIsInstance(self.tag.slug, str)

    def test_ingredient_model(self):
        """Проверяем поля модели ingredient."""
        self.assertIsInstance(self.ingredient.name, str)
        self.assertIsInstance(self.ingredient.measurement_unit, str)

    def test_recipe_model(self):
        """Проверяем поля модели recipe."""
        self.assertIsInstance(self.recipe.author, User)
        self.assertIsInstance(self.recipe.name, str)
        self.assertEquals(self.recipe.tags.count(), 1)
        self.assertEquals(self.recipe.ingredients.count(), 1)

    def test_ingredient_amount_model(self):
        """Проверяем поля модели ingredient_amount."""
        self.assertIsInstance(self.ingredient_amount.recipe, Recipe)
        self.assertIsInstance(self.ingredient_amount.ingredient, Ingredient)
        self.assertIsInstance(self.ingredient_amount.amount, int)

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        recipe = ModelTest.recipe
        self.assertEqual(len(recipe.__str__()), 6)
        tag = ModelTest.tag
        self.assertEqual(len(tag.__str__()), 3)
        ingredient = ModelTest.ingredient
        self.assertEqual(
            ingredient.__str__(),
            f'{self.ingredient.name}, {self.ingredient.measurement_unit}'
        )
