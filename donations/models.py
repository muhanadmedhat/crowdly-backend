from django.db import models
from projects.models import Project
from accounts.models import UserProfile

class Donations(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donationsapp_project')
    donor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='donationsapp_donor')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)