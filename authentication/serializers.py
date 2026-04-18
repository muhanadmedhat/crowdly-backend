from rest_framework import serializers
from accounts.models import UserProfile
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True)  
    password2 = serializers.CharField(write_only=True)  
    class Meta:
        model = UserProfile
        fields = [ 'username',
                   'email', 
                   'password', 
                   'password2', 
                   'phone', 
                   'country', 
                   'birth_date', 
                   'created_at',
                   'updated_at',
                   'is_staff',
                   'is_active']
        read_only_fields = ['created_at', 'updated_at', 'is_staff', 'is_active']
        
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        try:
            validate_password(attrs.get('password'))
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = UserProfile.objects.create_user(password=password,**validated_data)
        return user

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({"password": "Passwords do not match."})
        try:
            validate_password(attrs.get('password'))
        except DjangoValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'phone', 'country', 'birth_date', 'is_staff']