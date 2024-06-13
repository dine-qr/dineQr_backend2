from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Restaurant
from asgiref.sync import sync_to_async


# Account creation serializer
class RestaurantRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'email', 'password', 'first_name', 'last_name', 'phone_number', 
            'name', 'address', 'country', 'state', 'city','is_active'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        restaurant = Restaurant(**validated_data)
        restaurant.set_password(password)
        restaurant.role = 'restaurants' 
        restaurant.save()
        return restaurant

# Account login serializer
# class RestaurantLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)

#     async def validate(self, data):
#         email = data.get('email')
#         password = data.get('password')

#         if email and password:
#             # Use sync_to_async to call the authenticate function
#             user = await sync_to_async(authenticate)(request=self.context.get('request'), email=email, password=password)
#             if not user:
#                 raise serializers.ValidationError('Invalid credentials', code='authorization')
#         else:
#             raise serializers.ValidationError('Must include "email" and "password".')

#         data['user'] = user
#         return data


class RestaurantLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials', code='authorization')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        data['user'] = user
        return data

# All restuarant users serializer
class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'email', 'restaurant_owner', 'phone_number', 'address',
            'password', 'description', 'city', 'state', 'country',
            'zip_code', 'banner_image', 'logo', 'opening_hour', 'closing_hour',
            'custom_id', 'qr_code', 'tax_rate_percent', 'minimum_tax_product_price',
            'minimum_tax_rate_percent', 'restaurant_link', 'role', 
            'account_status', 'created_at'
        ]


class RestaurantUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'name', 'email', 'restaurant_owner', 'phone_number', 'address',
            'description', 'city', 'state', 'country', 'zip_code', 'banner_image',
            'logo', 'opening_hour', 'closing_hour', 'custom_id', 'qr_code',
            'tax_rate_percent', 'minimum_tax_product_price', 'minimum_tax_rate_percent',
            'restaurant_link', 'role', 'account_status'
        ]






# from django.contrib.auth import get_user_model
# from rest_framework import serializers
# from rest_framework.authtoken.models import Token
# from django.contrib.auth import authenticate

# User = get_user_model()

# class UserRegistrationSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

#     class Meta:
#         model = User
#         fields = ('email', 'first_name', 'last_name', 'password')

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             email=validated_data['email'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             password=validated_data['password']
#         )
#         # Token.objects.create(user=user)
#         return user

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()

#     def validate(self, data):
#         user = authenticate(username=data['email'], password=data['password'])
#         if not user:
#             raise serializers.ValidationError("Invalid login credentials")
#         return user
