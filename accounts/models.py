# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.IntegerField()
    balance = models.IntegerField(default=1000)
    # phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return str(self.user)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            account_number=random.randint(1000, 9999),
            balance=1000
        )