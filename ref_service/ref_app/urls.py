from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import ReferralCodeViewSet, ReferralViewSet, CustomUserViewSet, ReferralCodeByEmailView

router = DefaultRouter()
router.register(prefix='referral-codes', viewset= ReferralCodeViewSet, basename='ReferralCodeSerializer')
router.register(r'referrals', ReferralViewSet, 'ReferralSerializer')

urlpatterns = [
    path('', include(router.urls)),
    path('get-referral-code/', ReferralCodeByEmailView.as_view(), name='referral_code_by_email'),
    path('auth/register/', CustomUserViewSet.as_view({'post': 'create'}), name='user-register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
