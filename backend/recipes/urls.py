from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (FavoriteAPIView, IngredientsViewSet, RecipesViewSet,
                    TagsViewSet)

router = SimpleRouter()

router.register('tags', TagsViewSet)
router.register('ingredients', IngredientsViewSet)
router.register('recipes', RecipesViewSet)


urlpatterns = [
    path('recipes/<int:id>/favorite/', FavoriteAPIView.as_view(), name='favorite'),
    path('', include(router.urls)),
]
