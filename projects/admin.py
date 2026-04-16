from django.contrib import admin

from .models.project_model import Project

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ['title', 'creator', 'status', 'is_featured', 'created_at']
    list_editable = ['is_featured']
    list_filter   = ['status', 'is_featured']