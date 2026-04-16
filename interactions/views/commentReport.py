from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes , authentication_classes
from rest_framework.response import Response
from ..models import Comment , Rating , Reply , ProjectReport , CommentReport
from ..serializers import CommentSerializer , RatingSerializer , ReplySerializer , ProjectReportSerializer , CommentReportSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.db.models import Avg
from projects.models import Project

class CommentReportList(APIView):
  permission_classes = ([IsAuthenticated])
  def check(self , request , id , commentId):
    project = Project.objects.filter(id=id).first()
    if not project:
      return Response({"message":"There is no project with this id"}, status=status.HTTP_400_BAD_REQUEST)
    
    comment = Comment.objects.filter(id=commentId).first()
    if not comment:
      return Response({"message":"There is no comment with this id"}, status=status.HTTP_400_BAD_REQUEST)
    return comment
  
  def get(self,request,id,commentId):
    if request.user.is_staff != True:
      return Response({"message":"Invalid request"} , status=status.HTTP_403_FORBIDDEN)
    comment = self.check(request,id,commentId)
    if not isinstance(comment , Comment):
      return comment
    reports = CommentReport.objects.filter(comment=comment)
    reportsSerialized = CommentReportSerializer(reports , many=True)
    return Response(reportsSerialized.data , status=status.HTTP_200_OK)
  
  def post(self,request,id,commentId):
    comment = self.check(request,id,commentId)
    if not isinstance(comment , Comment):
      return comment
    reportSerialized = CommentReportSerializer(data = request.data)
    if reportSerialized.is_valid():
      reportSerialized.save(reporter = request.user , comment=comment)
      return Response(reportSerialized.data , status=status.HTTP_201_CREATED)
    else:
      return Response(reportSerialized.errors , status=status.HTTP_400_BAD_REQUEST)
  
    
    