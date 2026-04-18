from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField
class Category(models.Model):
    name        = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = CloudinaryField('image', folder='category',  blank=True, null=True
    )
    created_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.name