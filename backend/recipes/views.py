from rest_framework import viewsets

from .models import Ingridients, Recipe, Tag
from .serializers import (IngridientsListSerializer, RecipesListSerializer,
                          TagListSerializer)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagListSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingridients.objects.all()
    serializer_class = IngridientsListSerializer


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesListSerializer
