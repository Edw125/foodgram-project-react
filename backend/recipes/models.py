from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Tag(models.Model):
    name = models.CharField('Название', max_length=50)
    hex_color = models.CharField('Цвет', max_length=7)
    slug = models.SlugField('Адрес', max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        constraints = (
            models.UniqueConstraint(
                fields=['name', 'hex_color', 'slug'], name='unique tag',
            ),)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Продукт', max_length=200)
    measurement_unit = models.CharField('Единица измерения', max_length=200)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = (
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'], name='unique ingredient',
            ),)

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField('Название', max_length=200)
    image = models.ImageField('Картинка', upload_to='recipes/')
    text = models.TextField('Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientAmount',
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    tags = models.ManyToManyField(
        Tag, blank=True, related_name='recipes', verbose_name='Тег'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1, message='Время приготовления должно быть больше 1 минуты'
            ),
        ),
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        related_name='amounts',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество ингредиента',
        validators=(
            MinValueValidator(
                1, message='Количество продукта не может быть меньше 1'
            ),
        ),
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = (
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique ingredient amount'
            ),
        )


class Subscription(models.Model):
    subscriber = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscriber',
        verbose_name='Пользователь'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Автор рецепта'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=['subscriber', 'author'], name='unique subscription'
            ),
        )


class Favorites(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name="Рецепт"
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique favorites'
            ),
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        related_name='carts',
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'], name='unique shopping cart'
            ),
        )
