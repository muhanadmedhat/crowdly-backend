from .models import UserProfile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'username',
            'email',
            'phone',
            'profile_picture',
            'birth_date',
            'country',
            'created_at',
            'updated_at',
            'is_staff'
        ]
        read_only_fields = ['created_at', 'updated_at','is_staff']


    