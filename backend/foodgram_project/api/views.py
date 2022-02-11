from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import filters, status, viewsets

from django_filters.rest_framework import DjangoFilterBackend
from recipe.models import (AmountIngredientForRecipe, FavoriteRecipes,
                           Ingredient, Recipe, ShoppingCart, Tag)
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import MyRecipeFilter
from .paginator import MyPagePagination
from .permissions import OwnerOrAdminOrSafeMethods
from .serializers import (FavoriteRecipesSerializer, IngredientSerializer,
                          RecipeGETSerializer, RecipePOSTSerializer,
                          ShoppingCartSerializer, TagSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by('id')
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    permission_classes = (OwnerOrAdminOrSafeMethods,)
    pagination_class = MyPagePagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = MyRecipeFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeGETSerializer
        return RecipePOSTSerializer

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method != 'POST':
            get_object_or_404(
                FavoriteRecipes,
                user=request.user,
                recipe=get_object_or_404(Recipe, id=pk)
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = FavoriteRecipesSerializer(
            data={'user': request.user.id, 'recipe': pk},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method != 'POST':
            get_object_or_404(
                ShoppingCart,
                user=request.user,
                recipe=get_object_or_404(Recipe, id=pk)
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        serializer = ShoppingCartSerializer(
            data={'user': request.user.id, 'recipe': pk},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=(IsAuthenticated,)
    )
    def download_shopping_cart(self, request, pk=None):
        ingredients_dict = AmountIngredientForRecipe.objects.filter(
            recipe__user_shopping_cart__user=request.user.id
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_cart = ['Список покупок:\n--------------']
        position = 0
        for ingredient in ingredients_dict:
            position += 1
            shopping_cart.append(
                f'\n{position}. {ingredient["ingredient__name"]}:'
                f' {ingredient["amount"]}'
                f'({ingredient["ingredient__measurement_unit"]})'
            )
        response = HttpResponse(shopping_cart, content_type='text')
        response['Content-Disposition'] = (
            'attachment;filename=shopping_cart.pdf'
        )
        return response
