from django.db import models
from django.conf import settings
from .project_model import Project

class Donation(models.Model):
    project    = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='donations')
    donor      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='donations'
    )
    amount     = models.DecimalField(max_digits=10, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.donor} donated {self.amount} to {self.project}"