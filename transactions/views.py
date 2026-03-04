from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import TransferSerializer, DepositSerializer, WithdrawSerializer, ElectricitySerializer, WaterSerializer, InternetSerializer, MobileRechargeSerializer      

# transfer payment  
class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Transfer successful"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)

# deposit payment                   
class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Deposit successful"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)

# withdraw payment              
class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WithdrawSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Withdraw successful"},
                status=status.HTTP_200_OK
            )


        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)

# electricity payment           
class ElectricityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ElectricitySerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Electricity payment successful"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)

# water payment         
class WaterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WaterSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Water payment successful"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)

# internet payment      
class InternetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = InternetSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Internet payment successful"},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)

# mobile recharge   
class MobileRechargeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MobileRechargeSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Mobile recharge successful"},
                status=status.HTTP_200_OK
            )
    
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)

# transaction history   
class UserTransactionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(
            profile=self.request.user.profile
        ).order_by("-timestamp")