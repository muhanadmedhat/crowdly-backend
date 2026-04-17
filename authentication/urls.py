from django.contrib import admin
from django.urls import include,path
from .views import RegisterView,LoginView,EmailVerificationView,LogoutView,CookieTokenRefreshView,GoogleCallbackView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('google/callback/', GoogleCallbackView.as_view(), name='google_callback'),
    path('verify-token/', EmailVerificationView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', CookieTokenRefreshView.as_view())
]
