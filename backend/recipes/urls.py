from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import IngredientsViewSet, RecipesViewSet, TagsViewSet

router = SimpleRouter()

router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
