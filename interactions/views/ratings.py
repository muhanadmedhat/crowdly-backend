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

class ratingList(APIView):
  def check(self,request,id):
    project = Project.objects.filter(id=id).first()
    if not project:
      return Response({"message":"There is no project with this id"}, status=status.HTTP_400_BAD_REQUEST)
    return project
  
  def get(self,request,id):
    project = self.check(request , id)
    if not isinstance(project , Project):
      return project
    averageScore = Rating.objects.filter(project=project).aggregate(avg=Avg('score'))
    return Response(averageScore , status=status.HTTP_200_OK)
  
  def post(self,request,id):
    if not request.user.is_authenticated:
      return Response({"message":"Login needed first"} , status=status.HTTP_401_UNAUTHORIZED)
    project = self.check(request , id)
    if not isinstance(project , Project):
      return project
    ratingduplicated = Rating.objects.filter(user = request.user , project=project).first()
    if ratingduplicated:
      return Response({"message":"Duplicated rating for the same project"} , status=status.HTTP_400_BAD_REQUEST)
    ratingSerialized = RatingSerializer(data = request.data)
    if ratingSerialized.is_valid():
      ratingSerialized.save(user = request.user , project=project)
      return Response(ratingSerialized.data , status=status.HTTP_201_CREATED)
    else:
      return Response(ratingSerialized.errors , status=status.HTTP_400_BAD_REQUEST)
  
  def patch(self,request,id):
    if not request.user.is_authenticated:
      return Response({"message":"Login needed first"} , status=status.HTTP_401_UNAUTHORIZED)
    project = self.check(request , id)
    if not isinstance(project , Project):
      return project
    rating = Rating.objects.filter(user = request.user , project=project).first()
    if not rating:
      return Response({"message":"There is no rating for this project"} , status=status.HTTP_400_BAD_REQUEST)
    ratingSerialized = RatingSerializer(rating , data=request.data , partial=True)
    if ratingSerialized.is_valid():
      ratingSerialized.save()
      return Response(ratingSerialized.data , status = status.HTTP_200_OK)
    else:
      return Response(ratingSerialized.errors , status=status.HTTP_400_BAD_REQUEST)
    