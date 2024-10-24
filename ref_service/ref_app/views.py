from djoser.views import UserViewSet
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView

from .models import ReferralCode, User
from .serializers import ReferralCodeSerializer, UserRegistrationSerializer, \
    EmailRequestSerializer, ReferralRetrieveSerializer
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from asgiref.sync import sync_to_async



def clean_expired_referral_codes():
    ReferralCode.objects.filter(expiration_date__lt=timezone.now()).delete()


class ReferralCodeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReferralCodeSerializer
    queryset = ReferralCode.objects.none()

    def create(self, request):
        if hasattr(request.user, 'referralcode'):
            return Response({"error": "Referral code already exists."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    async def destroy(self, request, pk=None):
        referral_code = await ReferralCode.objects.get(user=request.user)
        referral_code.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReferralViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = ReferralRetrieveSerializer
    permission_classes = [permissions.IsAuthenticated]

    async def get_queryset(self):
        try:
            referral_code = await ReferralCode.objects.get(user=self.request.user)
            return self.queryset.filter(referral_code=referral_code)
        except ReferralCode.DoesNotExist:
            return self.queryset.none()


class CustomUserViewSet(UserViewSet):
    serializer_class = UserRegistrationSerializer


class ReferralCodeByEmailView(generics.GenericAPIView):
    serializer_class = EmailRequestSerializer

    async def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = await User.objects.get(email=email)
                referral_code = await ReferralCode.objects.get(user=user)
                return Response({'code': referral_code.code}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
            except ReferralCode.DoesNotExist:
                return Response({'error': 'Referral code not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


