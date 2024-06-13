from django.db import models

class Currency(models.Model):
    name = models.CharField(unique=True, max_length=255)
    country = models.CharField( max_length=255)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name