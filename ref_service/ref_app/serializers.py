from rest_framework import serializers
from .models import ReferralCode
from rest_framework import serializers
from .models import User, ReferralCode
from asgiref.sync import sync_to_async

class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ['code', 'expiration_date']


class ReferralRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class UserRegistrationSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField()

    class Meta:
        model = User
        fields = ['username', 'password', 'referral_code']
        extra_kwargs = {'password': {'write_only': True}}

    async def create(self, validated_data):
        code = validated_data.pop('referral_code')
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        try:
            referral_code = await ReferralCode.objects.get(code=code)
            if referral_code.is_active:
                user.referral_code = referral_code
            else:
                raise serializers.ValidationError("Реферальный код не активен.")
        except ReferralCode.DoesNotExist:
            raise serializers.ValidationError("Реферальный код не существует.")

        user.save()
        return user


