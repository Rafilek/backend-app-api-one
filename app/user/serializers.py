from django.contrib.auth import get_user_model

from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """serializers for the users objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'main_length': 5}}
    def create(self, validated_data):
        """Created a new user with encryptes password and return it"""
        return get_user_model().objects.create_user(**validated_data)    
