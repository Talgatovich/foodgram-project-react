from django.shortcuts import get_object_or_404
from rest_framework import status, views, viewsets
from rest_framework.response import Response

from .models import Favorite, Ingridients, Recipe, Tag
from .serializers import (FavoriteSerializer, IngridientsListSerializer,
                          RecipesCreateEditSerializer, RecipesListSerializer,
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
    actions_list = ['create', 'update']
    
    def get_serializer_class(self):
        if self.action in self.actions_list:
            return RecipesCreateEditSerializer
        return RecipesListSerializer


class FavoriteAPIView(views.APIView):

    def post(self, request, id):
        user_id = request.user.id
        data = {'user': user_id, 'recipe': id}
        serializer = FavoriteSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        deleting_obj = Favorite.objects.all().filter(user=user, recipe=recipe)
        if not deleting_obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        deleting_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
