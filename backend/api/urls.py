from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet

router_v1 = DefaultRouter()
router_v1.register('recipes', RecipesViewSet, basename='recipes')
router_v1.register('ingredients', IngredientsViewSet, basename='ingredients')
router_v1.register('tags', TagsViewSet, basename='tags')

urlpatterns = [
    path('', include(router_v1.urls)),

]
