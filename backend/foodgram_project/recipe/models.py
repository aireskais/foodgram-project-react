from django.core.validators import MinValueValidator
from django.db import models

from users.models import FoodgramUser


class Ingredient(models.Model):
    """
    Модель базовых Ингридиентов
    """
    name = models.CharField(max_length=200, db_index=True)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Модель Тега, цвет храним в виде НЕХ кода
    """
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, null=True)
    slug = models.SlugField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """
    Модель Рецепта:
    Ингредиенты и Теги - множественный, предустановленный список
    """
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='author'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='AmountIngredientForRecipe',
        through_fields=('recipe', 'ingredient'),
        related_name='ingredients'
    )
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='media/recipes/')
    text = models.TextField('recipe description')
    cooking_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1,
            message='Минимальное время готовки: 1 минута'
        )]
    )

    def __str__(self):
        return self.name


class AmountIngredientForRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(
            1,
            message='Минимальное количество: 1 единица'
        )]
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique_ingredient'
            ),
        )


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='user_shopping_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='user_shopping_cart'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            ),
        )

    def __str__(self):
        return f'{self.name} , {self.recipe}'


class FavoriteRecipes(models.Model):
    user = models.ForeignKey(
        FoodgramUser,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            ),
        )
