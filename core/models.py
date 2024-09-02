from django.db import models
from django.contrib.auth.models import User
import time

from django.core.mail import send_mail
from django.conf import settings
# Create your models here.


class Scrip(models.Model):
    scrip = models.CharField(max_length=15)

    def __str__(self):
        return self.scrip
    
class Alert(models.Model):
    user = models.ForeignKey(User, related_name="user_alert", on_delete=models.CASCADE)
    scrip = models.ForeignKey(Scrip, on_delete=models.CASCADE, related_name="scrip_alert")
    alert_on = models.IntegerField(max_length=6)
    today = models.FloatField(max_length=6)

    def check_and_send_alert(self):
        if self.alert_on <= self.today:
            self.send_alert()

    def send_alert(self):
        subject = f'Alert for {self.scrip}'
        message = f'Dear {self.user.username},\n\nYour alert for {self.scrip} has been triggered.'
        recipient_list = [self.user.email]
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)