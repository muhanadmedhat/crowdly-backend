from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes , authentication_classes
from rest_framework.response import Response
from .models import Comment , Rating , Reply , ProjectReport , CommentReport
from .serializers import CommentSerializer , RatingSerializer , ReplySerializer , ProjectReportSerializer , CommentReportSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import TokenAuthentication


# Create your views here.

# list comments for a project and add a comment
@api_view(['GET' , 'POST'])
@permission_classes([AllowAny])
def commentList(request,id):
  if request.method == 'GET':
    comments = Comment.objects.filter(project=id)
    commentsSerialized = CommentSerializer(comments , many=True)
    return Response({"comments":commentsSerialized.data} , status=status.HTTP_200_OK)
  else:
    if not request.user.is_authenticated:
      return Response({"message":"You must be logged in first"} , status=status.HTTP_401_UNAUTHORIZED)
    comment = CommentSerializer(data = request.data)
    if comment.is_valid():
      comment.save(author = request.user , project_id=id)
      return Response({"message":"Comment Created successfully"} , status=status.HTTP_201_CREATED)
    else:
      return Response(comment.errors , status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def deleteComment(request,id):
  comment = Comment.objects.filter(id=id)
  comment.delete()
  return Response({"message":"Deleted Successfully"} , status=status.HTTP_200_OK)


      
  