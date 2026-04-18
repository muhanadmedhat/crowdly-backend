from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserProfile
from rest_framework.pagination import CursorPagination
from rest_framework.throttling import UserRateThrottle
# Create your views here.
class UsersView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
           user = request.user
           token = request.COOKIES.get("refresh_token")
           user.delete()
           response = Response({"message": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
           if token:
               try:
                    refresh = RefreshToken(token)
                    refresh.blacklist()
               except:
                    pass
           response.delete_cookie (
               key="refresh_token",
               path='/',
               samesite='Lax'
           )
           return response
        
    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def patch(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserCursorPagination(CursorPagination):
    ordering = 'id'
    page_size = 12
class AdminsView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    throttle_classes = [UserRateThrottle]
    def get(self,request, id=None):
        if id is not None:
            try:
                user = UserProfile.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except UserProfile.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
                
        users = UserProfile.objects.all();
        paginator = UserCursorPagination()
        result = paginator.paginate_queryset(users,request)
        serializer = UserSerializer(result,many=True)
        return paginator.get_paginated_response(serializer.data)
    

    def delete(self, request, id=None):
        if id is None:
            return Response({"message": "User ID is required for deleting"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = UserProfile.objects.get(id=id) 
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        except UserProfile.DoesNotExist:          
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    def put(self, request, id=None):
        if id is None:
            return Response({"message": "User ID is required for updating"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = UserProfile.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save() 
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)