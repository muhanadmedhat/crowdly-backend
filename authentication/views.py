from rest_framework.views import APIView, Response, status
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.core import signing
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from .serializers import RegisterSerializer, UserSerializer, ResetPasswordSerializer
from accounts.models import UserProfile
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .utils import send_verification_email, verify_token,reset_verify_token,send_reset_password
# Create your views here.

class RegisterView(APIView):
    throttle_classes = [AnonRateThrottle]
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if (serializer.is_valid()):
            user = serializer.save()
            send_verification_email(user)
            return Response({"message": "check your email"}, status=201)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    throttle_classes = [AnonRateThrottle]
    def post(self,request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = UserProfile.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response("wrong credentials", status=401)
        if not user.is_active:
            send_verification_email(user)
            return Response("account not verified, check your email", status=403)
        refresh = RefreshToken.for_user(user)
        refresh['is_staff'] = user.is_staff  
        serializer = UserSerializer(user)
        response = Response({
            'access': str(refresh.access_token),
            'user': serializer.data
        })
        response.set_cookie (
            key='refresh_token',
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite='None',
            max_age=7 * 24 * 60 * 60
        )
        return response
    
class EmailVerificationView(APIView):
    throttle_classes = [AnonRateThrottle]
    def get(self,request):
        token = request.query_params.get('token')
        try:
            user_pk = verify_token(token)
            user = UserProfile.objects.get(pk=user_pk)
            if user.is_active:
                return Response({"message": "account is already verified"}, status=200)
            user.is_active = True
            user.save()
            return Response({"message": "account verified"}, status=200)
        except Exception:
            return Response({"message": "invalid or expired token"}, status=400)

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"message": "email is required"}, status=400)       
        user = UserProfile.objects.filter(email=email).first()
        if not user:
            return Response({"message": "if the email exists, a verification link has been sent"}, status=200)  
        if user.is_active:
            return Response({"message": "account is already verified"}, status=400)
        send_verification_email(user)
        return Response({"message": "verification email sent"}, status=200)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def post(self, request):
        token = request.COOKIES.get("refresh_token")
        if not token:
            return Response({"message": "no token"}, status=400)
        try:
            refresh = RefreshToken(token) 
            refresh.blacklist()
            response = Response({"message": "logged out"}, status=200)
            response.delete_cookie(
                key='refresh_token',
                path='/',
                samesite='Lax'
            )
            return response
        except Exception:
            return Response({"message": "invalid token"}, status=400)
        
class CookieTokenRefreshView(TokenRefreshView):
    throttle_classes = [AnonRateThrottle]
    def post(self,request):
        token = request.COOKIES.get("refresh_token")
        if not token:
            return Response({"message": "no token"}, status=400)
        
        try:
            data = request.data.copy() 
            data['refresh'] = token
            serializer = self.get_serializer(data=data)
            try:
                serializer.is_valid(raise_exception=True)
            except TokenError as e:
                raise InvalidToken(e.args[0])

            new_access = serializer.validated_data.get('access')
            new_refresh = serializer.validated_data.get('refresh')
            response = Response({'access': new_access}, status=status.HTTP_200_OK)
    
            if new_refresh:
                response.set_cookie(
                    key='refresh_token',
                    value=str(new_refresh),
                    httponly=True,
                    # secure=True,  
                    samesite='Lax',
                    max_age=7 * 24 * 60 * 60
                )
            return response
        except Exception as e:
            return Response({"message": str(e)}, status=400)
        
class GoogleCallbackView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "postmessage" 
    client_class = OAuth2Client
class SendResetPasswordView(APIView):
    throttle_classes = [AnonRateThrottle]        
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"message": "email is required"}, status=status.HTTP_400_BAD_REQUEST)
        user = UserProfile.objects.filter(email=email).first()
        if user:
            send_reset_password(user)
        return Response({"message": "if the email exists, a reset link has been sent"}, status=status.HTTP_200_OK)
class ResetPasswordConfirmView(APIView):
    def get(self,request):
        uid = request.query_params.get("uid")
        token = request.query_params.get("token")
        if not uid or not token:
            return Response({"message": "invalid or expired link"}, status=status.HTTP_400_BAD_REQUEST)
        user = reset_verify_token(uid, token)
        if user:
            return Response({"message": "valid token"}, status=200)
        return Response({"message": "invalid or expired link"}, status=400)
        
    def post(self,request):
        uid = request.data.get("uid")
        token = request.data.get("token")
        user = reset_verify_token(uid, token)
        if not user:
            return Response({"message": "failed to reset password (expired link)"}, status=400)
        
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            first_error = list(serializer.errors.values())[0][0] if serializer.errors else "invalid password format"
            return Response({"message": first_error}, status=400)
        
        password = serializer.validated_data.get("password")
        user.set_password(password)
        user.save()
        return Response({"message": "password updated successfully"}, status=200)
