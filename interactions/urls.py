
from django.contrib import admin
from django.urls import path
from .views import CommentReportList , commentList , userComments , projectReportList,ratingList,replyList,userReplies,replyReportList

urlpatterns = [
    path('projects/<int:id>/comments/' , commentList , name="commentList"),
    path('projects/<int:id>/comments/<int:commentId>/', userComments.as_view(), name="userComments"),
    path('projects/<int:id>/comments/<int:commentId>/replies/' , replyList.as_view() , name="replyList"),
    path('projects/<int:id>/comments/<int:commentId>/replies/<int:replyId>/', userReplies.as_view() , name="userReplies"),
    path('projects/<int:id>/ratings/' , ratingList.as_view() , name="ratingList"),
    path('projects/<int:id>/reports/' , projectReportList.as_view() , name="projectReportList"),
    path('projects/<int:id>/comments/<int:commentId>/reports/' , CommentReportList.as_view() , name="commentReportList"),
    path('projects/<int:id>/comments/<int:commentId>/replies/<int:replyId>/reports/' , replyReportList.as_view() , name="replyReportList")    
]
