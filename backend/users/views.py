from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import mixins, serializers, viewsets

from .models import Follow
from .serializers import FollowSerializer

User = get_user_model()


class CreateListViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet
):

    pass


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        user = get_object_or_404(User, id=user_id)
        new_queryset = user.follower
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
