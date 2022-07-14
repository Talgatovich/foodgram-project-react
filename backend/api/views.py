from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, views, viewsets
from rest_framework.response import Response

from .permissions import AuthorOrAdmin, ReadOnly
from .serializers import (
    FavoriteSerializer,
    FollowCreateSerializer,
    FollowListSerializer,
    IngridientListSerializer,
    RecipesCreateSerializer,
    RecipesListSerializer,
    ShoppingCartSerializer,
    TagListSerializer,
)
from .utils import create_ingredients_list, dowload_list

from users.models import Follow  # isort:skip
from recipes.models import Favorite, Ingridient, Tag  # isort:skip
from recipes.models import ShoppingCart  # isort: skip
from recipes.models import Recipe  # isort:skip

User = get_user_model()


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagListSerializer
    permission_classes = [
        ReadOnly,
    ]


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingridient.objects.all()
    serializer_class = IngridientListSerializer
    permission_classes = [
        ReadOnly,
    ]
    filter_backends = [
        filters.SearchFilter,
    ]
    search_fields = ("^name",)


class RecipesViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesListSerializer
    permission_classes = [
        AuthorOrAdmin,
    ]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("tags__name",)
    actions_list = ["POST", "PATCH"]

    def get_permissions(self):
        if self.action == "retrieve":
            return (ReadOnly(),)
        return super().get_permissions()

    def get_serializer_class(self):
        if self.request.method in self.actions_list:
            return RecipesCreateSerializer
        return RecipesListSerializer


class FavoriteAPIView(views.APIView):
    permission_classes = [AuthorOrAdmin]

    def post(self, request, id):
        user_id = request.user.id
        data = {"user": user_id, "recipe": id}
        serializer = FavoriteSerializer(
            data=data, context={"request": request}
        )
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


class ShoppingCartAPIView(views.APIView):
    def post(self, request, id):
        user_id = request.user.id
        data = {"user": user_id, "recipe": id}
        serializer = ShoppingCartSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        deleting_obj = ShoppingCart.objects.all().filter(
            user=user, recipe=recipe
        )
        if not deleting_obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        deleting_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCartAPIView(views.APIView):
    def get(self, request):
        user = request.user
        recipes_in_cart = ShoppingCart.objects.all().filter(user=user)
        create_ingredients_list(recipes_in_cart)
        file_location = "./api/Ingredients_list.txt"
        return dowload_list(file_location)


class FollowCreateAPIView(views.APIView):
    def post(self, request, id):
        user_id = request.user.id
        data = {"user": user_id, "following": id}
        serializer = FollowCreateSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(User, id=id)
        deleting_obj = Follow.objects.all().filter(
            user=user, following=following
        )
        if not deleting_obj:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        deleting_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListAPIView(generics.ListAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowListSerializer

    def get_queryset(self):
        user = self.request.user
        new_queryset = User.objects.all().filter(following__user=user)
        return new_queryset
