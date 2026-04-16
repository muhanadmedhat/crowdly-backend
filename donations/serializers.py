from .models import Donations
from rest_framework import serializers
class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donations
        fields = "__all__"
        read_only_fields = ['donor', 'project']