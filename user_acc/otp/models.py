from django.db import models
# from ..customers.models import Customers


class Otp(models.Model):
    code = models.PositiveIntegerField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField()
    # user = models.ForeignKey(Customers, on_delete=models.CASCADE)

    