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
  project = models.ForeignKey(Project , on_delete=models.CASCADE)
  reporter = models.ForeignKey('accounts.UserProfile' , on_delete=models.CASCADE)
  reason = models.CharField(max_length=20 , choices=Reason_Choices , default='other')
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.project} , {self.reporter} , {self.reason}"
  

class CommentReport(models.Model):
  Reason_Choices = [
    ('spam' , 'Spam'),
    ('inappropriate' , 'Inappropriate Content'),
    ('harassment' , 'Harassment'),
    ('other' , 'Other')
  ]
  comment = models.ForeignKey(Comment , on_delete=models.CASCADE)
  reporter = models.ForeignKey('accounts.UserProfile' , on_delete=models.CASCADE)
  reason = models.CharField(max_length=30 , choices=Reason_Choices , default='other')
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.comment} , {self.reporter} , {self.reason}"
  
class ReplyReport(models.Model):
  Reason_Choices = [
  ('spam' , 'Spam'),
  ('inappropriate' , 'Inappropriate Content'),
  ('harassment' , 'Harassment'),
  ('other' , 'Other')
  ]
  reply = models.ForeignKey(Reply , on_delete=models.CASCADE)
  reporter = models.ForeignKey('accounts.UserProfile' , on_delete=models.CASCADE)
  reason = models.CharField(max_length=30 , choices=Reason_Choices , default='other')
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.reply} , {self.reporter} , {self.reason}"

  