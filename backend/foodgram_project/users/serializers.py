from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Follow, FoodgramUser
from recipe.models import Recipe


class FoodgramUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodgramUser
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, following):
        return Follow.objects.filter(
            user=self.context.get('request').user,
            following=following
        ).exists()


class FoodgramUserCreateSerializer(UserCreateSerializer):
    """ Сериализация пользователя при регистрации """
    class Meta:
        model = FoodgramUser
        fields = (
            'email', 'username', 'first_name', 'last_name', 'password'
        )


class FollowListSerializer(serializers.ModelSerializer):
    """ Сериализация списка на кого подписан пользователь"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = FoodgramUser
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, following):
        return Recipe.objects.filter(author=following).count()

    def get_recipes(self, following):
        queryset = self.context.get('request')
        recipes_limit = queryset.query_params.get('recipes_limit')
        if not recipes_limit:
            return RecipeFollowingSerializer(
                following.author.all(),
                many=True, context={'request': queryset}
            ).data
        return RecipeFollowingSerializer(
            following.author.all()[:int(recipes_limit)], many=True,
            context={'request': queryset}
        ).data

    def get_is_subscribed(self, following):
        return Follow.objects.filter(
            user=self.context.get('request').user,
            following=following
        ).exists()


class RecipeFollowingSerializer(serializers.ModelSerializer):
    """ Сериализация списка рецептов на кого подписан пользователь """
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    """ Сериализация при подписке на пользователя """
    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate(self, data):
        get_object_or_404(FoodgramUser, username=data['following'])
        if self.context['request'].user == data['following']:
            raise serializers.ValidationError('Сам на себя подписываешься!')
        if Follow.objects.filter(
                user=self.context['request'].user,
                following=data['following']
        ):
            raise serializers.ValidationError('Уже подписан')
        return data

    def to_representation(self, instance):
        return FollowListSerializer(
            instance.following,
            context={'request': self.context.get('request')}
        ).data
