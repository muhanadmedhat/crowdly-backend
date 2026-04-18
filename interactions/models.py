from django.db import models
from django.conf import settings
from projects.models import Project

# Create your models here.

class Comment(models.Model):
  project = models.ForeignKey(Project , on_delete=models.CASCADE)
  author = models.ForeignKey('accounts.UserProfile' , on_delete=models.CASCADE)
  text = models.TextField(max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
     return f"{self.project} , {self.author} = {self.text}"

class Reply(models.Model):
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
  author = models.ForeignKey('accounts.UserProfile' , on_delete=models.CASCADE)
  text = models.TextField(max_length=500)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.author} {self.comment} {self.text}"


class Rating(models.Model):
  project = models.ForeignKey(Project , on_delete=models.CASCADE)
  user = models.ForeignKey('accounts.UserProfile' , on_delete=models.CASCADE)
  score = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  
  class Meta:
    unique_together = ('project','user')
  
  def __str__(self):
      return f"{self.project} , {self.user} = {self.score}"


class ProjectReport(models.Model):
  Reason_Choices = [
    ('spam' , 'Spam'),
    ('inappropriate' , 'Inappropriate Content'),
    ('fraud' , 'Fraud'),
    ('other' , 'Other')
  ]
  Status_Choices = [
    ('pending', 'Pending Review'),
    ('reviewed', 'Reviewed'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
  ]
  project = models.ForeignKey(Project , on_delete=models.CASCADE)
  reporter = models.ForeignKey('accounts.UserProfile' , on_delete=models.CASCADE)
  reason = models.CharField(max_length=20 , choices=Reason_Choices , default='other')
  status = models.CharField(max_length=20, choices=Status_Choices, default='pending')
  admin_notes = models.TextField(blank=True, null=True, help_text='Admin notes about the report action')
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.project} , {self.reporter} , {self.reason} - {self.status}"
  

class CommentReport(models.Model):
  Reason_Choices = [
    ('spam' , 'Spam'),
    ('inappropriate' , 'Inappropriate Content'),
    ('harassment' , 'Harassment'),
    ('other' , 'Other')
  ]
  Status_Choices = [
    ('pending', 'Pending Review'),
    ('reviewed', 'Reviewed'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
  ]
  comment = models.ForeignKey(Comment , on_delete=models.CASCADE)
  reporter = models.ForeignKey('accounts.UserProfile' , on_delete=models.CASCADE)
  reason = models.CharField(max_length=30 , choices=Reason_Choices , default='other')
  status = models.CharField(max_length=20, choices=Status_Choices, default='pending')
  admin_notes = models.TextField(blank=True, null=True, help_text='Admin notes about the report action')
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.comment} , {self.reporter} , {self.reason} - {self.status}"
  
class ReplyReport(models.Model):
  Reason_Choices = [
  ('spam' , 'Spam'),
  ('inappropriate' , 'Inappropriate Content'),
  ('harassment' , 'Harassment'),
  ('other' , 'Other')
  ]
  Status_Choices = [
    ('pending', 'Pending Review'),
    ('reviewed', 'Reviewed'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
  ]
  reply = models.ForeignKey(Reply , on_delete=models.CASCADE)
  reporter = models.ForeignKey('accounts.UserProfile' , on_delete=models.CASCADE)
  reason = models.CharField(max_length=30 , choices=Reason_Choices , default='other')
  status = models.CharField(max_length=20, choices=Status_Choices, default='pending')
  admin_notes = models.TextField(blank=True, null=True, help_text='Admin notes about the report action')
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.reply} , {self.reporter} , {self.reason} - {self.status}"