from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, views, viewsets
from rest_framework.response import Response

from .models import Favorite, Ingridients, Recipe, ShoppingCart, Tag
from .permissions import AuthorOrAdmin, ReadOnly
from .serializers import (
    FavoriteSerializer,
    IngridientsListSerializer,
    RecipesCreateSerializer,
    RecipesListSerializer,
    ShoppingCartSerializer,
    TagListSerializer,
)


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagListSerializer


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingridients.objects.all()
    serializer_class = IngridientsListSerializer


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
        data = {"user": user_id, "recipes": id}
        serializer = FavoriteSerializer(
            data=data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        recipe = get_object_or_404(Recipe, id=id)
        deleting_obj = Favorite.objects.all().filter(user=user, recipes=recipe)
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

    def get(self, request):
        ingridients = {}
        user = request.user
        recipes_in_cart = ShoppingCart.objects.all().filter(user=user)

        for obj in recipes_in_cart:
            recipe = obj.recipe.recipe
            for val in recipe.all():
                name = val.ingredient.name
                amount = val.amount
                measurement_unit = val.ingredient.measurement_unit
                if name not in ingridients:
                    ingridients[name] = {
                        "measurement_unit": measurement_unit,
                        "amount": amount,
                    }
                else:
                    ingridients[name]["amount"] += amount

        with open("Ingredients_list.txt", "w", encoding="utf-8") as file:
            for key in ingridients:
                file.write(
                    (
                        f'{key} - {ingridients[key]["amount"]}'
                        f'{ingridients[key]["measurement_unit"]} \n'
                    )
                )

        file_location = "./Ingredients_list.txt"
        try:
            with open(file_location, "r", encoding="utf-8") as f:
                file_data = f.read()

            response = HttpResponse(file_data, content_type="text/plain")
            response[
                "Content-Disposition"
            ] = 'attachment; filename="Ingredients_list.txt"'
        except IOError:
            response = HttpResponseNotFound("<h1>File not exist</h1>")
        return response
