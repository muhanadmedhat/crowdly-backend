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
from decimal import Decimal
stripe.api_key = settings.STRIPE_SECRET_KEY

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
    
class DonationCheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, project_id):
        amount = request.data.get("amount")
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'egp',
                        'product_data': {
                            'name': f'Donation to Project #{project_id}',
                        },
                        'unit_amount': int(float(amount) * 100), 
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=f'{settings.FRONTEND_URL}donation/success?session_id={{CHECKOUT_SESSION_ID}}',
                cancel_url=f'{settings.FRONTEND_URL}donation/cancel',
                payment_intent_data={
                    'metadata': {
                        'project_id': project_id,
                        'donor_id': request.user.id,
                    }
                },
                metadata={
                    'project_id': project_id,
                    'donor_id': request.user.id,
                }
            )
            
            return Response({
                'checkout_url': checkout_session.url,
                'session_id': checkout_session.id
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=400)


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
            try:
                project_id = int(intent['metadata']['project_id'])
                donor_id = int(intent['metadata']['donor_id'])

                amount = Decimal(str(intent['amount'])) / Decimal('100')

                with transaction.atomic():
                    project = Project.objects.get(id=project_id)
                    donor = UserProfile.objects.get(id=donor_id)
                    Donations.objects.create(
                        donor=donor,
                        project=project,
                        amount=amount
                    )
                    project.total_donated = (project.total_donated or Decimal('0')) + amount
                    project.save()
            except Exception as e:
                import traceback
                return Response({'error': str(e)}, status=500)

        return Response({'status': 'ok'})