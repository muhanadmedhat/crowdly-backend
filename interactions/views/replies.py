from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes , authentication_classes
from rest_framework.response import Response
from ..models import Comment , Rating , Reply , ProjectReport , CommentReport
from ..serializers import CommentSerializer , RatingSerializer , ReplySerializer , ProjectReportSerializer , CommentReportSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from projects.models import Project

class replyList(APIView):
  def check(self , request , id , commentId):
    project = Project.objects.filter(id=id).first()
    if not project:
      return Response({"message":"There is no project with this id"}, status=status.HTTP_400_BAD_REQUEST)
    
    comment = Comment.objects.filter(id=commentId).first()
    if not comment:
      return Response({"message":"There is no comment with this id"}, status=status.HTTP_400_BAD_REQUEST)
    
    return comment
  
  def get(self,request,id,commentId):
    comment = self.check(request , id , commentId)
    if not isinstance(comment , Comment):
      return comment
    replies = Reply.objects.filter(comment=comment)
    repliesSerialized = ReplySerializer(replies , many=True)
    return Response({"replies":repliesSerialized.data} , status=status.HTTP_200_OK)
  
  def post(self,request,id,commentId):
    if not request.user.is_authenticated:
      return Response({"message":"Login needed first"} , status=status.HTTP_401_UNAUTHORIZED)
    comment = self.check(request , id , commentId)
    if not isinstance(comment , Comment):
      return comment
    replySerialized = ReplySerializer(data=request.data)
    if replySerialized.is_valid():
      replySerialized.save(author = request.user , comment = comment)
      return Response(replySerialized.data , status=status.HTTP_201_CREATED)
    else:
      return Response(replySerialized.errors , status=status.HTTP_400_BAD_REQUEST)

class userReplies(APIView):
    permission_classes = ([IsAuthenticated])
    def check(self , request , id , commentId , replyId):
      project = Project.objects.filter(id=id).first()
      if not project:
        return Response({"message":"There is no project with this id"}, status=status.HTTP_400_BAD_REQUEST)

      comment = Comment.objects.filter(id=commentId).first()
      if not comment:
        return Response({"message":"There is no comment with this id"}, status=status.HTTP_400_BAD_REQUEST)

      reply = Reply.objects.filter(id=replyId).first()
      if not reply:
        return Response({"message":"There is no reply with this id"}, status=status.HTTP_400_BAD_REQUEST)
      if reply.author != request.user:
        return Response({"message":"Unallowed action"}, status=status.HTTP_403_FORBIDDEN) 
      return reply
    
    def patch(self,request,id,commentId , replyId):
      reply = self.check(request , id , commentId , replyId)
      if not isinstance(reply , Reply):
        return reply
      replySerialized = ReplySerializer(reply ,data=request.data , partial=True)
      if replySerialized.is_valid():
        replySerialized.save()
        return Response({"message":"Reply updated"} , status=status.HTTP_200_OK)
      else:
        return Response(replySerialized.errors , status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self,request,id,commentId , replyId):
      reply = self.check(request , id , commentId , replyId)
      if not isinstance(reply , Reply):
        return reply
      reply.delete()
      return Response({"message":"Deleted Successfully"} , status=status.HTTP_200_OK)
      
    