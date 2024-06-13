from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt import views as simple_jwt_views
# from .views import MyTokenObtainPairView
from rest_framework.routers import DefaultRouter

from user_acc.currency.views import CurrencyViewSet
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



router = routers.DefaultRouter()

router.register(r'auth/restaurants',RestaurantRegisterView , basename='restaurants')
router.register(r'currency', CurrencyViewSet, basename='currency')

# from django.urls import path
# from .restaurant.views import RestaurantRegisterView, RestaurantLoginView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('auth/register/', RestaurantRegisterView.as_view(), name='restaurant-register'),
    path('auth/login/', RestaurantLoginView.as_view(), name='restaurant-login'),

    path('restaurant_user/<int:id>/', GetUserByIDView.as_view(), name='get-user-by-id'),
    path('restaurant_user/update/<int:id>/', UpdateRestaurantView.as_view(), name='update-restaurant'),

]

# urlpatterns += router.urls

