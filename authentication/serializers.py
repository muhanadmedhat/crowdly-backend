from rest_framework import serializers
from accounts.models import UserProfile
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
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password');
        user = UserProfile.objects.create_user(password=password,**validated_data)
        return user