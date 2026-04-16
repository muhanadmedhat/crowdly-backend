import stripe
from django.conf import settings
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import CursorPagination
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from .serializers import DonationSerializer
from projects.models import Project
from accounts.models import UserProfile
from .models import Donations
from django.db import transaction
# Create your views here.
class donationsPaginator(CursorPagination):
    ordering = 'id'
    page_size = 12
class adminView(APIView):
    permission_classes = [IsAuthenticated,IsAdminUser]
    def get(self,request,id=None):
        if id is not None:
            try:
                donatation = Donations.objects.get(id=id)
                serializer = DonationSerializer(donatation)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Donations.DoesNotExist:
                return Response({"error": "Donation not found"}, status=status.HTTP_404_NOT_FOUND)
        donations = Donations.objects.all().select_related('donor', 'project')
        paginator = donationsPaginator()
        result= paginator.paginate_queryset(donations,request)
        serializer = DonationSerializer(result,many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def delete(self,request,id):
        if id is None:
            return Response({"error": "id not found!"},status=status.HTTP_400_BAD_REQUEST)
        try:
            donation = Donations.objects.get(id=id)
            donation.delete()
        except Donations.DoesNotExist:
            return Response({"error": "Donation not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self,request,id):
        if id is None:
            return Response({"error": "id not found!"},status=status.HTTP_400_BAD_REQUEST)
        try:
            donation = Donations.objects.get(id=id)
        except Donations.DoesNotExist:
            return Response({"error": "Donation not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = DonationSerializer(donation, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class userView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,id=None):
        if id is not None:
            try:
                donatation = Donations.objects.get(id=id, donor=request.user)
                serializer = DonationSerializer(donatation)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Donations.DoesNotExist:
                return Response({"error": "Donation not found"}, status=status.HTTP_404_NOT_FOUND)
        donations = Donations.objects.filter(donor=request.user).select_related('donor', 'project')
        paginator = donationsPaginator()
        result= paginator.paginate_queryset(donations,request)
        serializer = DonationSerializer(result,many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request, project_id):
        project = Project.objects.get(id=project_id)
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(donor=request.user, project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class donationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, project_id):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        amount = request.data.get("amount")
        intent = stripe.PaymentIntent.create(
            amount=int(float(amount) * 100),
            currency='egp',
            metadata={'project_id': project_id, 'donor_id': request.user.id}
        )
        return Response({'client_secret': intent.client_secret})


class StripeWebhookView(APIView):
    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
            )
        except Exception:
            return Response(status=400)
        if event['type'] == 'payment_intent.succeeded':
            intent = event['data']['object']
            project_id = intent['metadata']['project_id']
            donor_id = intent['metadata']['donor_id']
            amount = intent['amount'] / 100

            with transaction.atomic():
                project = Project.objects.get(id=project_id)
                donor = UserProfile.objects.get(id=donor_id)
                Donations.objects.create(
                    donor=donor,
                    project=project,
                    amount=amount
                )
                project.total_donated += amount
                project.save()

        return Response({'status': 'ok'})