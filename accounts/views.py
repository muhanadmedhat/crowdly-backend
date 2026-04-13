from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework import status
from .models import UserProfile
# Create your views here.
class UsersView(APIView):
    def get(self,request):
        users = UserProfile.objects.all();
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self, request):
        # email = request.data.get('email', '')
        # if email.endswith('@blocked.com'):
        #     return Response(
        #         {"email": "Registrations from this domain are not allowed."},
        #         status=status.HTTP_403_FORBIDDEN
        #     )
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id):
        try:
            user = UserProfile.objects.get(id=id) 
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)  
        except UserProfile.DoesNotExist:          
            return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self,request,id):
        try:
            user = UserProfile.objects.get(id=id)
            serializer = UserSerializer(user,data=request.data,partial=True)
            if (serializer.is_valid()):
                serializer.save() 
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
