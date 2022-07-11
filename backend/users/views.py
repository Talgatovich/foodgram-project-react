from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, views
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowCreateSerializer, FollowListSerializer

User = get_user_model()


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
