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

    sender = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="sent_transactions",
        null=True,
        blank=True
    )

    receiver = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="received_transactions",
        null=True,
        blank=True
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="transactions")
    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(default=timezone.now)

