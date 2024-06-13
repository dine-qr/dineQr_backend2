from rest_framework.serializers import ModelSerializer
from .models import Currency

class CurrencySerializers(ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"