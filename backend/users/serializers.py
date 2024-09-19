from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirmation', 'role', 'usn', 'branch']
        extra_kwargs = {
            'password': {'write_only': True},
            'usn': {'required': False},
            'branch': {'required': False}
        }

    def validate_branch(self, value):
        allowed_branches = ['CS', 'IS', 'AIML', 'Mechanical']
        if value not in allowed_branches:
            raise serializers.ValidationError("Invalid branch selected.")
        return value

    def validate(self, data):
        if data['password'] != data['password_confirmation']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')  # Remove confirmation field
        user = User(**validated_data)
        user.set_password(validated_data['password'])  # Ensure password is hashed
        user.save()
        return user

    
    
