from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Follow
from .serializers import FollowCreateSerializer

User = get_user_model()

class FollowViewSet(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = FollowCreateSerializer

    def get_queryset(self):
        user = self.request.user
        #user = get_object_or_404(User, id=user_id)
        new_queryset = Follow.objects.all().filter(user=user)
        return new_queryset

