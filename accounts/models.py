# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

def generate_account_number():
    last_profile = Profile.objects.order_by('-account_number').first()
    if last_profile:
        return last_profile.account_number + 1
    return 10000

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.IntegerField(unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    fcm_token = models.TextField(blank=True, null=True)
    # phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return str(self.user)


    # def withdraw(self, amount):
    #     if amount > self.balance:
    #         raise ValidationError("Insufficient funds. Cannot withdraw beyond available balance.")
    #     self.balance -= amount
    #     self.save()

    # def deposit(self, amount):
    #     self.balance += amount
    #     self.save()



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            account_number=generate_account_number(),
            balance=1000
        )