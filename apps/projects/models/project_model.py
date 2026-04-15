from django.db import models
from django.conf import settings
from .category_model import Category
from .tag_model import Tag

class Project(models.Model):
    STATUS_CHOICES = [
        ('running',   'Running'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    title         = models.CharField(max_length=200)
    details       = models.TextField()
    category      = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags          = models.ManyToManyField(Tag, blank=True)
    total_target  = models.DecimalField(max_digits=12, decimal_places=2)
    total_donated = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    creator       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    start_time    = models.DateTimeField()
    end_time      = models.DateTimeField()
    status        = models.CharField(max_length=20, choices=STATUS_CHOICES, default='running')
    is_featured   = models.BooleanField(default=False)
    created_at    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title