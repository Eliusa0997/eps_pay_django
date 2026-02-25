from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import ValidationError
from accounts.models import Profile
from .models import Transaction


class TransferSerializer(serializers.Serializer):
    account_number = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        sender_profile = request.user.profile

        try:
            receiver_profile = Profile.objects.get(
                account_number=validated_data['account_number']
            )
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Receiver not found.")

        amount = validated_data['amount']

        if sender_profile.balance < amount:
            raise serializers.ValidationError("Insufficient balance.")

        with transaction.atomic():

            # Deduct from sender
            sender_profile.balance -= amount
            sender_profile.save()

            # Add to receiver
            receiver_profile.balance += amount
            receiver_profile.save()

            # Record transactions
            Transaction.objects.create(
                profile=sender_profile,
                transaction_type='transfer',
                amount=amount
            )

            Transaction.objects.create(
                profile=receiver_profile,
                transaction_type='deposit',
                amount=amount
            )

        return validated_data
