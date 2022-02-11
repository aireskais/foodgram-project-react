from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField
from recipe.models import (AmountIngredientForRecipe, FavoriteRecipes,
                           Ingredient, Recipe, ShoppingCart, Tag)
from users.serializers import FoodgramUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class AmountIngredientForRecipeGETSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit', read_only=True
    )
    id = serializers.IntegerField(source='ingredient.id', read_only=True)

    class Meta:
        model = AmountIngredientForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AmountIngredientForRecipePOSTSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1)

    class Meta:
        model = AmountIngredientForRecipe
        fields = ('id', 'amount')


class RecipeGETSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = FoodgramUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField(
        method_name='get_ingredients'
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients', 'is_favorited',
            'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time'
        )

    def get_ingredients(self, recipe):
        return AmountIngredientForRecipeGETSerializer(
            AmountIngredientForRecipe.objects.filter(recipe=recipe),
            many=True
        ).data

    def get_is_favorited(self, recipe):
        return FavoriteRecipes.objects.filter(
            user=self.context.get('request').user,
            recipe=recipe
        ).exists()

    def get_is_in_shopping_cart(self, recipe):
        return ShoppingCart.objects.filter(
            user=self.context.get('request').user,
            recipe=recipe
        ).exists()


class RecipePOSTSerializer(serializers.ModelSerializer):
    author = FoodgramUserSerializer(read_only=True)
    ingredients = AmountIngredientForRecipePOSTSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    image = Base64ImageField(represent_in_base64=True)

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'ingredients', 'tags',
                  'image', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(
            author=self.context.get('request').user,
            **validated_data
        )
        for ingredient in ingredients:
            AmountIngredientForRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        for tag in tags:
            recipe.tags.add(tag)
        return recipe

    def update(self, recipe, validated_data):
        recipe.tags.clear()
        AmountIngredientForRecipe.objects.filter(recipe=recipe).delete()
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        for ingredient in ingredients:
            AmountIngredientForRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )
        for tag in tags:
            recipe.tags.add(tag)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        return RecipeGETSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data


class FavoriteRecipesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipes
        fields = ('user', 'recipe')

    def validate(self, data):
        if FavoriteRecipes.objects.filter(
                user=self.context.get('request').user,
                recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError({
                'status': 'Уже добавлен'
            })
        return data

    def to_representation(self, instance):
        return RecipeViewSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class RecipeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')

    def validate(self, data):
        if ShoppingCart.objects.filter(
                user=self.context['request'].user,
                recipe=data['recipe']
        ):
            raise serializers.ValidationError('Уже добавлен')
        return data

    def to_representation(self, instance):
        return RecipeViewSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data
