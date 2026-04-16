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

class projectReportList(APIView):
  permission_classes=([IsAuthenticated])
  def check(self,request,id):
    project = Project.objects.filter(id=id).first()
    if not project:
      return Response({"message":"There is no project with this Id"} , status=status.HTTP_404_NOT_FOUND)
    return project
  
  def post(self,request,id):
    project = self.check(request,id)
    if not isinstance(project,Project):
      return project
    reportSerialized = ProjectReportSerializer(data = request.data)
    if reportSerialized.is_valid():
      reportSerialized.save(reporter = request.user , project = project)
      return Response(reportSerialized.data , status=status.HTTP_201_CREATED)
    else:
      return Response(reportSerialized.errors , status=status.HTTP_400_BAD_REQUEST)
    
  def get(self,request,id):
    if request.user.is_staff != True:
      return Response({"message":"Invalid request"} , status=status.HTTP_403_FORBIDDEN)
    project = self.check(request,id)
    if not isinstance(project,Project):
      return project
    reports = ProjectReport.objects.filter(project = project)
    reportsSerialized = ProjectReportSerializer(reports , many=True)
    return Response(reportsSerialized.data , status=status.HTTP_200_OK)
    