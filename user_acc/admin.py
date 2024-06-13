from django.contrib import admin
from .restaurants.models import Restaurant, Staff, Customer

# Assuming each model has specific admin needs, or you could use a generic approach as above
class RestaurantAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Restaurant._meta.fields]

class StaffAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Staff._meta.fields]

class CustomerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Customer._meta.fields]

admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Customer, CustomerAdmin)
