from django.urls import path
from .views import adminView, userView, donationView, StripeWebhookView

urlpatterns = [
    path('admin/', adminView.as_view()),
    path('admin/<int:id>/', adminView.as_view()),
    path('me/', userView.as_view()),
    path('me/<int:id>/', userView.as_view()),
    path('projects/<int:project_id>/pay/', donationView.as_view()),
    path('webhook/', StripeWebhookView.as_view()),
]
