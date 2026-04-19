from django.urls import path
from .views import adminView, userView, DonationCheckoutView, StripeWebhookView

urlpatterns = [
    path('admin/', adminView.as_view()),
    path('admin/<int:id>/', adminView.as_view()),
    path('me/', userView.as_view()),
    path('me/<int:id>/', userView.as_view()),
    path('checkout/<int:project_id>/', DonationCheckoutView.as_view()),
    path('webhook/', StripeWebhookView.as_view()),
]
