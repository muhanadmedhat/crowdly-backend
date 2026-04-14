from django.contrib import admin
from django.urls import path
from .views import UsersView
urlpatterns = [
    path('', UsersView.as_view()),
    path('<int:id>/',UsersView.as_view())
]