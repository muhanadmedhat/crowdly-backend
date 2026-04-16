from django.db import models
from django.conf import settings
from .category_model import Category
from .tag_model import Tag

class Project(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='projects',
        blank=True
    )

    title = models.CharField(max_length=200)
    details = models.TextField()
    total_target = models.DecimalField(max_digits=12, decimal_places=2)
    total_donated = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    is_cancelled = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title