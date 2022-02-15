import django_filters
from rest_framework.filters import SearchFilter

from recipe.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    tags = django_filters.AllValuesMultipleFilter(field_name='tags__slug')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')


class IngredientFilter(SearchFilter):
    search_param = 'name'
