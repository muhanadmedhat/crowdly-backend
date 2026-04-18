from rest_framework import serializers

from accounts.serializers import UserSerializer
from projects.projectSerializers import ProjectDetailSerializer
from .models import Comment , Rating , Reply , ProjectReport , CommentReport , ReplyReport

class CommentSerializer(serializers.ModelSerializer):
  author = UserSerializer(read_only=True)
  project = ProjectDetailSerializer(read_only=True)
  class Meta:
    model = Comment
    fields = '__all__'
    read_only_fields = ['id','project','author','created_at','updated_at']
    
class ReplySerializer(serializers.ModelSerializer):
  author = UserSerializer(read_only=True)
  comment = CommentSerializer(read_only=True)
  class Meta:
    model = Reply
    fields = '__all__'
    read_only_fields = ['id','author','comment','created_at','updated_at']

class RatingSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)
  project = ProjectDetailSerializer(read_only=True)
  class Meta:
    model = Rating
    fields = '__all__'
    read_only_fields = ['id','project', 'user' , 'created_at']
  def validate_score(self,value):
    if value < 1 or value > 5:
      raise serializers.ValidationError("Rating must be between 1 and 5")
    return value

class ProjectReportSerializer(serializers.ModelSerializer):
  reporter = UserSerializer(read_only=True)
  project = ProjectDetailSerializer(read_only=True)
  class Meta:
    model = ProjectReport
    fields = ['id', 'reporter', 'project', 'reason', 'created_at', 'status', 'admin_notes']
    read_only_fields = ['id', 'project', 'reporter', 'created_at', 'status', 'admin_notes']
    
class CommentReportSerializer(serializers.ModelSerializer):
  reporter = UserSerializer(read_only=True)
  comment = CommentSerializer(read_only=True)
  class Meta:
    model = CommentReport
    fields = ['id', 'reporter', 'comment', 'reason', 'created_at', 'status', 'admin_notes']
    read_only_fields = ['id', 'comment', 'reporter', 'created_at', 'status', 'admin_notes']

class ReplyReportSerializer(serializers.ModelSerializer):
  reporter = UserSerializer(read_only=True)
  reply = ReplySerializer(read_only=True)
  class Meta:
    model = ReplyReport
    fields = ['id', 'reporter', 'reply', 'reason', 'created_at', 'status', 'admin_notes']
    read_only_fields = ['id', 'reply', 'reporter', 'created_at', 'status', 'admin_notes']