from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer, ForgotPasswordInitiateSerializer, \
      ForgotPasswordVerifyOtpSerializer, ForgotPasswordSetPinSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PasswordResetSerializer
from .restaurants.views import *
from .otp.models import Otp
import random
import string
from django.utils import timezone
from .restaurants.controller import RestaurantController
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import make_password





# @staticmethod
# def generate_otp():
#     otp = ''.join(random.choices(string.digits, k=6))
#     return otp

# class MyTokenObtainPairView(TokenObtainPairView):   
#     serializer_class = MyTokenObtainPairSerializer


# class PasswordResetView(generics.CreateAPIView):
#     serializer_class = PasswordResetSerializer
#     permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             user = request.user
#             new_password = serializer.validated_data['new_password']

#             user.set_password(new_password)
#             user.save()

#             return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ForgotPasswordInitiateView(generics.CreateAPIView):
#     serializer_class = ForgotPasswordInitiateSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             email = serializer.validated_data['email']
#             try: 
#                 res_instance = Users.objects.get(email=email)
#             except Users.DoesNotExist:
#                 return Response({'message': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
#             try:
#                 code_exists = Otp.objects.get(email=email)
#                 if code_exists:
#                     code_exists.delete()    
#             except Otp.DoesNotExist:
#                 pass

            
#             otp_code = generate_otp()
            
#             try: 
#                 res_instance = Users.objects.get(email=email)
#                 expiration_time = timezone.now() + timezone.timedelta(minutes=10)
#                 otp_instance = Otp.objects.create(email=email, code=otp_code, timestamp=expiration_time)
#                 RestaurantController.send_forgot_password_otp_email(email, res_instance.name, otp_code)
#             except Restaurants.DoesNotExist:
#                 return Response({'message': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        
                
#                 # return Response({'message': 'Otp model doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)
            
#             return Response({'message': 'Otp sent successfully'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



# class ForgotPasswordVerifyCodeView(generics.CreateAPIView):
#     serializer_class = ForgotPasswordVerifyOtpSerializer
#     # permission_classes = [IsAuthenticated]

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             otp = serializer.validated_data['otp']
#             email = serializer.validated_data['email']
#             try:
#                 user = Users.objects.get(email=email)
#             except Users.DoesNotExist:
#                 return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

#             try: 
#                 code_exists = Otp.objects.get(code=otp, email=email)
                
#                 if code_exists.timestamp < timezone.now():
#                     return Response({'message': 'OTP has expired.'}, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     res = Users.objects.get(email=email)
#                     res.is_verified_for_forgot_password_reset = True
#                     res.save()
#                     code_exists.delete()
#                     return Response({'message': 'Verification successful. You can proceed to resetting the password'}, status=status.HTTP_200_OK)

#             except:
#                 return Response({'message': 'Invalid Otp'}, status=status.HTTP_404_NOT_FOUND)
                
          
#         else:
#             return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

   

# class ForogtPasswordSetPinView(APIView):
#     @swagger_auto_schema(request_body=ForgotPasswordSetPinSerializer)
#     def post(self, request, *args, **kwargs):
#         serializer = ForgotPasswordSetPinSerializer(data=request.data)
#         if serializer.is_valid():
#             password = serializer.validated_data['new_password']
#             email = serializer.validated_data['email']

#             try:
#                 res = Users.objects.get(email=email)   
#                 if res.is_verified_for_forgot_password_reset == True:
#                     encrypted_pin = make_password(password)
#                     res.password  = encrypted_pin
#                     res.save()
#                     RestaurantController.send_forgot_password_email_successful(email, res.name)

#                     return Response({'message': 'Password successfully set.'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'message': 'Restaurant account has not been verified for forgot password'})

#             except Users.DoesNotExist:
#                 return Response({'message': 'User with this email not found.'}, status=status.HTTP_404_NOT_FOUND)

#         return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
