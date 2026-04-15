from django.db import models
from django.conf import settings
from .project_model import Project

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image   = models.ImageField(upload_to='media/projects/')
    order   = models.IntegerField(default=0)

    def __str__(self):
        return f"Image for {self.project.title} (order {self.order})"