from rest_framework import serializers
from .models import Comment , Rating , Reply , ProjectReport , CommentReport

class CommentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'
    read_only_fields = ['id','author','created_at','updated_at']
    
class ReplySerializer(serializers.ModelSerializer):
  class Meta:
    model = Reply
    fields = '__all__'
    read_only_fields = ['id','author','created_at','updated_at']

class RatingSerializer(serializers.ModelSerializer):
  class Meta:
    model = Rating
    fields = '__all__'
    read_only_fields = ['id', 'user' , 'created_at']

class ProjectReportSerializer(serializers.ModelSerializer):
  class Meta:
    model = ProjectReport
    fields = '__all__'
    read_only_fields = ['id' , 'reporter']
    
class CommentReportSerializer(serializers.ModelSerializer):
  class Meta:
    model = CommentReport
    fields = '__all__'
    read_only_fields = ['id','reporter' , 'created_at']