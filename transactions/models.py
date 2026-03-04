from django.db import models

# Create your models here.

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from accounts.models import Profile


class Transaction(models.Model):

    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('transfer', 'Transfer'),
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('internet', 'Internet'),
        ('mobile_recharge', 'Mobile Recharge'),
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):

        if self.amount <= 0:
            raise ValidationError("Amount must be greater than zero.")

        if self.transaction_type == "deposit":
            self.profile.balance += self.amount

        elif self.transaction_type == "withdraw":
            if self.amount > self.profile.balance:
                raise ValidationError("Insufficient balance.")
            self.profile.balance -= self.amount

        self.profile.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
