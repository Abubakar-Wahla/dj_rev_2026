from django.db import models
from django.contrib.auth.models import User
import uuid

class Tag(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name="projects")
    title=models.CharField(max_length=200)
    description=models.TextField(max_length=500,blank=True,null=True)
    tags=models.ManyToManyField(Tag,blank=True,related_name="projects")
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

    
