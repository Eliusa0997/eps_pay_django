from rest_framework import serializers
from django.db import transaction
from django.core.exceptions import ValidationError
from accounts.models import Profile
from .models import Transaction


from django.db import transaction

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

            sender_profile.balance -= amount
            sender_profile.save()

            receiver_profile.balance += amount
            receiver_profile.save()

            # sender transaction
            Transaction.objects.create(
                profile=sender_profile,
                sender=sender_profile,
                receiver=receiver_profile,
                transaction_type='transfer',
                amount=amount
            )

            # receiver transaction
            Transaction.objects.create(
                profile=receiver_profile,
                sender=sender_profile,
                receiver=receiver_profile,
                transaction_type='deposit',
                amount=amount
            )

        return validated_data


class DepositSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        amount = validated_data['amount']

        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(
                user=request.user
            )

            profile.balance += amount
            profile.save()

            Transaction.objects.create(
                profile=profile,
                transaction_type='deposit',
                amount=amount
            )

        return {
            "status": "success",
            "amount": amount,
            "new_balance": profile.balance
        }



class WithdrawSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        amount = validated_data['amount']

        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(
                user=request.user
            )

            if profile.balance < amount:
                raise serializers.ValidationError("Insufficient balance.")

            profile.balance -= amount
            profile.save()

            Transaction.objects.create(
                profile=profile,
                transaction_type='withdraw',
                amount=amount
            )

        return {
            "status": "success",
            "amount": amount,
            "new_balance": profile.balance
        }


class ElectricitySerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        amount = validated_data['amount']

        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(
                user=request.user
            )

            if profile.balance < amount:
                raise serializers.ValidationError("Insufficient balance.")

            profile.balance -= amount
            profile.save()

            Transaction.objects.create(
                profile=profile,
                transaction_type='electricity',
                amount=amount
            )

        return {
            "status": "success",
            "amount": amount,
            "new_balance": profile.balance
        }


class WaterSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        amount = validated_data['amount']

        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(
                user=request.user
            )

            if profile.balance < amount:
                raise serializers.ValidationError("Insufficient balance.")

            profile.balance -= amount
            profile.save()

            Transaction.objects.create(
                profile=profile,
                transaction_type='water',
                amount=amount
            )

        return {
            "status": "success",
            "amount": amount,
            "new_balance": profile.balance
        }


class InternetSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        amount = validated_data['amount']

        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(
                user=request.user
            )

            if profile.balance < amount:
                raise serializers.ValidationError("Insufficient balance.")

            profile.balance -= amount
            profile.save()

            Transaction.objects.create(
                profile=profile,
                transaction_type='internet',
                amount=amount
            )

        return {
            "status": "success",
            "amount": amount,
            "new_balance": profile.balance
        }


class MobileRechargeSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate(self, data):
        if data['amount'] <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return data

    def create(self, validated_data):
        request = self.context['request']
        amount = validated_data['amount']

        with transaction.atomic():
            profile = Profile.objects.select_for_update().get(
                user=request.user
            )

            if profile.balance < amount:
                raise serializers.ValidationError("Insufficient balance.")

            profile.balance -= amount
            profile.save()

            Transaction.objects.create(
                profile=profile,
                transaction_type='mobile_recharge',
                amount=amount
            )

        return {
            "status": "success",
            "amount": amount,
            "new_balance": profile.balance
        }       


class TransactionSerializer(serializers.ModelSerializer):

    sender_full_name = serializers.SerializerMethodField()
    receiver_full_name = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "transaction_type",
            "amount",
            "timestamp",
            "receiver_full_name"
        ]

    def get_sender_full_name(self, obj):
        if obj.sender and obj.sender.user:
            return f"{obj.sender.user.first_name} {obj.sender.user.last_name}"
        return None

    def get_receiver_full_name(self, obj):
        if obj.receiver and obj.receiver.user:
            return f"{obj.receiver.user.first_name} {obj.receiver.user.last_name}"
        return None