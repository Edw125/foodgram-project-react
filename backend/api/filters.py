from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipe


class IngredientSearchFilter(SearchFilter):
    search_param = 'name'


class RecipeFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(method='filter_is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def filter_is_favorited(self, queryset, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(is_favorited=self.request.user)
        return queryset

    def filter_is_in_shopping_cart(self, queryset, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(is_in_shopping_cart=self.request.user)
        return queryset
