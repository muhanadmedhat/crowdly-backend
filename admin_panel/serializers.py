from rest_framework import serializers
from interactions.models import ProjectReport, CommentReport, ReplyReport
from projects.models import Category



class ReportActionSerializer(serializers.Serializer):
    """Serializer for admin actions on reports"""
    action = serializers.ChoiceField(
        choices=['approve', 'reject'],
        help_text="Action to take: 'approve' (mark as reviewed) or 'reject' (false report)"
    )
    admin_notes = serializers.CharField(
        max_length=500,
        required=False,
        allow_blank=True,
        help_text="Optional notes about the action"
    )


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for project categories"""
    projects_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'projects_count']
        extra_kwargs = {
            'name': {'max_length': 100},
            'description': {'required': False, 'allow_blank': True}
        }
    
    def get_projects_count(self, obj):
        """Return count of projects in this category"""
        return obj.projects.count()
