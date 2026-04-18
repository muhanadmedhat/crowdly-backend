from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes , authentication_classes
from rest_framework.response import Response
from ..models import Comment , Rating , Reply , ProjectReport , CommentReport , ReplyReport
from ..serializers import CommentSerializer , RatingSerializer , ReplySerializer , ProjectReportSerializer , CommentReportSerializer, ReplyReportSerializer
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from django.db.models import Avg
from projects.models import Project
from rest_framework.pagination import CursorPagination

class ReplyReportPagination(CursorPagination):
  ordering ='created_at'
  page_size=5

class replyReportList(APIView):
  permission_classes = ([IsAuthenticated])
  def check(self,request,id,commentId,replyId):
    project = Project.objects.filter(id=id).first()
    if not project:
      return Response({"message":"There is no project with this id"}, status=status.HTTP_400_BAD_REQUEST)
    
    comment = Comment.objects.filter(id=commentId).first()
    if not comment:
      return Response({"message":"There is no comment with this id"}, status=status.HTTP_400_BAD_REQUEST)
    reply = Reply.objects.filter(id=replyId).first()
    if not reply:
      return Response({"message":"There is no reply with this id"}, status=status.HTTP_400_BAD_REQUEST)
    return reply
  
  def get(self,request,id,commentId,replyId):
    if request.user.is_staff != True:
      return Response({"message":"Invalid request"} , status=status.HTTP_403_FORBIDDEN)
    reply = self.check(request,id,commentId,replyId)
    if not isinstance(reply,Reply):
      return reply
    repliesReport = ReplyReport.objects.filter(reply=reply)
    paginator = ReplyReportPagination()
    result = paginator.paginate_queryset(repliesReport , request)
    repliesReportSerialized = ReplyReportSerializer(result , many=True)
    return paginator.get_paginated_response(repliesReportSerialized.data)
  
  def post(self,request,id,commentId,replyId):
    reply = self.check(request,id,commentId,replyId)
    if not isinstance(reply,Reply):
      return reply
    replyReport = ReplyReportSerializer(data = request.data)
    if replyReport.is_valid():
      replyReport.save(reporter = request.user , reply=reply)
      return Response(replyReport.data , status=status.HTTP_201_CREATED)
    else:
      return Response(replyReport.errors , status=status.HTTP_400_BAD_REQUEST)
    