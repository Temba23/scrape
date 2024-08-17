from django.db import models
from django.contrib.auth.models import User
import time
# Create your models here.

class Alert(models.Model):
    user = models.ForeignKey(User, related_name="user_alert", on_delete=models.CASCADE)
    scrip = models.CharField(max_length=15)
    alert_on = models.IntegerField(max_length=6)
    date = models.CharField(max_length=50, default='-')
    today = models.IntegerField(max_length=6)