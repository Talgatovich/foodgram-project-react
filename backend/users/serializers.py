from rest_framework import serializers

from .models import User


class UserListSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = User
        fields = ("id", "email", "username", "first_name", "last_name")
        
class UserSerializer(serializers.ModelSerializer):
    
    class Meta():
        model = User
        fields = ("id", "email", "username", "first_name", "last_name", "password")
