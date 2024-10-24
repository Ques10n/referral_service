from django.utils import timezone
from .models import ReferralCode  # Замените на ваше приложение

def clean_expired_referral_codes():
    ReferralCode.objects.filter(expiration_date__lt=timezone.now()).delete()

def clean_referral_codes_middleware(get_response):
    clean_expired_referral_codes()
    def middleware(request):
        response = get_response(request)
        return response

    return middleware