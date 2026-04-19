from django.contrib import admin

from .models import Category, Tag, Project

# Register your models here.
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display  = ['title', 'owner', 'created_at']
admin.site.register(Category)
admin.site.register(Tag)