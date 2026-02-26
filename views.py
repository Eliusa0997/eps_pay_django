from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password,email=email)
    return Response({'message': 'User created successfully'}, status=201)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Simple API to get profile data of logged-in user
    """
    profile = request.user.profile
    
    data = {
        'username': request.user.username,
        'account_number': profile.account_number,
        'balance': str(profile.balance),  # Convert to string for JSON
        # 'phone_number': profile.phone_number,  # Uncomment if you add this field
    }
    
    return Response(data, status=status.HTTP_200_OK)