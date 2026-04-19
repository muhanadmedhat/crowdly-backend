from .models import UserProfile
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'phone',
            'profile_picture',
            'birth_date',
            'country',
            'created_at',
            'updated_at',
            'is_staff',
            'is_active'
        ]
        read_only_fields = ['created_at', 'updated_at','is_staff', 'is_active']


    