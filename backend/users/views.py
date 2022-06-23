from rest_framework import viewsets

from .models import User
from .serializers import UserListSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    actions_list = ['retrieve', 'list']
    
    def get_serializer_class(self):
        if self.action in self.actions_list:
            return UserListSerializer
        return UserSerializer
