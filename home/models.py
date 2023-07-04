from django.db import models
from django.contrib.auth.models import AbstractUser
# import uuid

class User(AbstractUser):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255,unique=True)
    password=models.CharField(max_length=255)
    username=models.CharField(max_length=255,unique=True)
    category=models.CharField(max_length=7)

    REQUIRED_FIELDS=[]

class Document(models.Model):
    ids = models.AutoField(primary_key=True)
    caption=models.TextField()
    teacher = models.CharField(max_length=255)
    student=models.CharField(max_length=255)
# Create your models here.
