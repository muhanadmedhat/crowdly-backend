from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes , authentication_classes
from rest_framework.response import Response
from ..models import Comment
from ..serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from projects.models import Project
from utils.pagination import CustomCursorPagination

# Create your views here.
# add get comment for special user
# list comments for a project and add a comment
class CommentPagination(CustomCursorPagination):
  ordering = 'created_at'
  page_size = 5
@api_view(['GET' , 'POST'])
@permission_classes([AllowAny])
def commentList(request,id):
  project = Project.objects.filter(id=id).first()
  if not project:
    return Response({"message":"There is no project with this id"}, status=status.HTTP_400_BAD_REQUEST)
  
  if request.method == 'GET':
    comments = Comment.objects.filter(project=project)
    paginator = CommentPagination()
    result = paginator.paginate_queryset(comments,request)
    commentsSerialized = CommentSerializer(result , many=True)
    return paginator.get_paginated_response(commentsSerialized.data)
  else:
    if not request.user.is_authenticated:
      return Response({"message":"You must be logged in first"} , status=status.HTTP_401_UNAUTHORIZED)
    
    comment = CommentSerializer(data = request.data)
    if comment.is_valid():
      comment.save(author = request.user , project=project)
      return Response(comment.data , status=status.HTTP_201_CREATED)
    else:
      return Response(comment.errors , status=status.HTTP_400_BAD_REQUEST)

class userComments(APIView):
  permission_classes = ([IsAuthenticated])
  
  def check(self , request , id , commentId):
    project = Project.objects.filter(id=id).first()
    if not project:
      return Response({"message":"There is no project with this id"}, status=status.HTTP_400_BAD_REQUEST)
    
    comment = Comment.objects.filter(id=commentId).first()
    if not comment:
      return Response({"message":"There is no comment with this id"}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.user != comment.author :
      return Response({"message":"Unallowed action"}, status=status.HTTP_403_FORBIDDEN)
    return comment
  
  def patch(self , request , id , commentId):
    comment = self.check(request , id , commentId)
    if not isinstance(comment , Comment):
      return comment
    commentSerialized = CommentSerializer(comment , data=request.data, partial=True)
    if commentSerialized.is_valid():
      commentSerialized.save()
      return Response({"message":"Comment updated successfully"} , status=status.HTTP_200_OK)
    else:
      return Response(commentSerialized.errors , status=status.HTTP_400_BAD_REQUEST)
  
  def delete(self , request , id , commentId):
    comment = self.check(request , id , commentId)
    if not isinstance(comment , Comment):
      return comment
    comment.delete()
    return Response({"message":"Deleted successfully"} , status=status.HTTP_200_OK)
      


      
  
