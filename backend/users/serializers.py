from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Use your custom User model
        fields = ['email', 'password', 'role', 'usn', 'branch']
        extra_kwargs = {
            'password': {'write_only': True},
            'usn': {'required': False},
            'branch': {'required': False}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Ensure password is hashed
        user.save()
        return user
    
    
    
