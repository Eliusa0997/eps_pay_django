from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from accounts.models import Profile 
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer  

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
    return Response({'message': 'User created successfully'}, status=201)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    API to get profile data and recent transactions of logged-in user
    """
    profile = request.user.profile

    # Get recent 5 transactions (latest first)
    recent_transactions = Transaction.objects.filter(profile=profile).order_by('-timestamp')[:5]
    transactions_serializer = TransactionSerializer(recent_transactions, many=True)

    data = {
        'username': request.user.username,
        'full_name': f"{request.user.first_name} {request.user.last_name}",
        'account_number': profile.account_number,
        'balance': str(profile.balance),  # Convert Decimal to string for JSON
        'email': request.user.email,
        'date_joined': request.user.date_joined,   
        'recent_transactions': transactions_serializer.data
    }

    return Response(data, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_receiver_by_account_number(request):
    account_number = request.data.get('account_number')

    if not account_number:
        return Response(
            {"error": "Account number is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        profile = Profile.objects.select_related('user').get(
            account_number=account_number
        )

        data = {
            "username": profile.user.username,
            "account_number": profile.account_number,
        }

        return Response(data, status=status.HTTP_200_OK)

    except Profile.DoesNotExist:
        return Response(
            {"error": "Receiver not found"},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_fcm_token(request):
    fcm_token = request.data.get("fcm_token")

    profile = request.user.profile
    profile.fcm_token = fcm_token
    profile.save()

    return Response({"message": "FCM token saved successfully"})