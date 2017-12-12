from django.db import models
import time
# Create your models here.
class Action(models.Model):
    time = models.CharField(max_length=30, default= time.strftime('%Y-%m-%dT%H:%M:%S',time.localtime(time.time())))
    action_type = models.CharField(max_length=30) #sleep or cry