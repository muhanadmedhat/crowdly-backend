from .models import Donations
from rest_framework import serializers

class DonationSerializer(serializers.ModelSerializer):
    project_title = serializers.CharField(source='project.title', read_only=True)
    
    class Meta:
        model = Donations
        fields = "__all__"
        read_only_fields = ['donor', 'project']
