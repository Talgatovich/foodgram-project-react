from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()

class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')   

class RegisterUserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'username', 'first_name', 'last_name')          
