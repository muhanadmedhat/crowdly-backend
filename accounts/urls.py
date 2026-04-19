from django.contrib import admin
from django.urls import path
from .views import UsersView,AdminsView
from projects.projectViews import MyProjectsAPIView

urlpatterns = [
    path('me/projects/', MyProjectsAPIView.as_view()),
    path('me/', UsersView.as_view()),
    path('<int:id>/', AdminsView.as_view()),
    path('', AdminsView.as_view())
]