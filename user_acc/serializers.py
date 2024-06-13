from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import Token
from rest_framework import serializers
# from .customers.models import Customers
from django.contrib.auth import authenticate


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email
        token['user_id'] = user.id
        
        response = {
            "user_id": user.id,
            "token": token
        }
        return response


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         data = super().validate(attrs)
#         refresh = self.get_token(self.user)
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#         data['user_id'] = self.user.id
#         data['email'] = self.user.email
#         return data


 
class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField()


class ForgotPasswordInitiateSerializer(serializers.Serializer):
    email = serializers.CharField()


class ForgotPasswordVerifyOtpSerializer(serializers.Serializer):
    otp = serializers.CharField()
    email = serializers.CharField()


class ForgotPasswordSetPinSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    email = serializers.CharField()
