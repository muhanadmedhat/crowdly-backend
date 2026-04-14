from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import UserProfile
from rest_framework.pagination import CursorPagination
# Create your views here.
class UserCursorPagination(CursorPagination):
    ordering = 'id'
class UsersView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), IsAdminUser()]
        return [IsAuthenticated()]
    
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
            if request.user.id != id and not request.user.is_staff:
                return Response({"message": "not allowed"}, status=403)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        except UserProfile.DoesNotExist:          
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self,request, id=None):
        if id is None:
            return Response({"message": "User ID is required for updating"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = UserProfile.objects.get(id=id)
            if request.user.id != id and not request.user.is_staff:
                return Response({"message": "not allowed"}, status=403)
            serializer = UserSerializer(user,data=request.data,partial=True)
            if (serializer.is_valid()):
                serializer.save() 
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
