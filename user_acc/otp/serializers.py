from rest_framework.serializers import ModelSerializer
from .models import Otp


class OtpSerializers(ModelSerializer):
    class Meta:
        model = Otp
        fields = "__all__"