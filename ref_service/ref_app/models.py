from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    referral_code = models.ForeignKey('ReferralCode',
                                      on_delete=models.CASCADE,
                                      blank= True,
                                      null=True,
                                      related_name='+',)

    # REQUIRED_FIELDS = ['referral_code']



class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')
    code = models.CharField(max_length=10, unique=True)
    expiration_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default= True)

    def __str__(self):
        return self.code




