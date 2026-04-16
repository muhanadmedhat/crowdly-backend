from django.db import models
from projects.models import Projects
from accounts.models import UserProfile

class Donations(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    donor = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)