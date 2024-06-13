
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import Restaurant
from .serializers import *
from asgiref.sync import sync_to_async
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from adrf.decorators import APIView


class RestaurantRegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new restaurant",
        request_body=RestaurantRegistrationSerializer,
        responses={201: 'Account created successfully', 400: 'Invalid data'}
    )
    async def post(self, request):
        serializer = RestaurantRegistrationSerializer(data=request.data)
        is_valid = await sync_to_async(serializer.is_valid)()
        if is_valid:
            try:
                restaurant = await sync_to_async(serializer.save)()
                refresh = RefreshToken.for_user(restaurant)
                return Response({
                    'message': 'Restaurant registered successfully',
                    'id': restaurant.id,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class RestaurantLoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login",
        request_body=RestaurantLoginSerializer,
        responses={200: 'User logged in successfully', 401: 'Invalid credentials', 400: 'Invalid data'}
    )
    async def post(self, request):
        serializer = RestaurantLoginSerializer(data=request.data, context={'request': request})
        is_valid = await sync_to_async(serializer.is_valid)()
        if is_valid:
            try:
                validated_data = serializer.validated_data
                user = validated_data['user']
                refresh = RefreshToken.for_user(user)
                return Response({
                    "id": user.id,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Update user
class UpdateRestaurantView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    async def put(self, request, id):
        restaurant = await sync_to_async(get_object_or_404)(Restaurant, id=id)
        serializer = RestaurantUpdateSerializer(restaurant, data=request.data, partial=True)
        if await sync_to_async(serializer.is_valid)():
            await sync_to_async(serializer.save)()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserByIDView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    async def get(self, request, id):
        user = await sync_to_async(get_object_or_404)(Restaurant, id=id)
        serializer = RestaurantSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


