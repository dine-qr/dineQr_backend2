

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.files import File
from io import BytesIO
import qrcode
import uuid
import string
import random
from dineqr.settings import MOBILE_APP_URL
# from ..currency.models import Currency
# from ..roles.models import Roles

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.password = make_password(password) 
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=2500, null=True, blank=True)
    last_name = models.CharField(max_length=2500, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=2000, null=True, blank=True)
    state = models.CharField(max_length=2000, null=True, blank=True)
    country = models.CharField(max_length=2000, null=True, blank=True)
    zip_code = models.PositiveBigIntegerField(null=True, blank=True)
    profile_image = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    is_phonenumber_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='%(class)s_set', 
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='%(class)s_set', 
        blank=True
    )
    
    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        abstract = True
        

    def generate_custom_id(self):
        if not self.custom_id:
            self.custom_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.qr_code_url())
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        buffer.seek(0)

        filename = f"{self.name}_qr_code.png"
        self.qr_code.save(filename, File(buffer), save=False)

    def qr_code_url(self):
        app_url = MOBILE_APP_URL
        return f"{app_url}/{self.custom_id}/homepage"

    def __str__(self):
        return self.email


class Restaurant(BaseUser):
    name = models.CharField(max_length=2000, unique=True)
    restaurant_owner = models.CharField(max_length=2000)

    description = models.TextField(null=True, blank=True)
    banner_image = models.TextField(null=True, blank=True)
    image_one = models.TextField(null=True, blank=True)
    image_two = models.TextField(null=True, blank=True)
    image_three = models.TextField(null=True, blank=True)
    logo = models.TextField(null=True, blank=True)
    opening_hour = models.DateTimeField(null=True, blank=True)
    closing_hour = models.DateTimeField(null=True, blank=True)
    custom_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    qr_code = models.ImageField(upload_to='restaurants/qr_codes/', null=True, blank=True)
    restaurant_link = models.TextField(null=True, blank=True)
    next_subscription_date = models.DateField(null=True, blank=True)
    paystack_recipient_code = models.TextField(null=True, blank=True)
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE, null=True, blank=True)
    tax_rate_percent = models.DecimalField(decimal_places=2, max_digits=6, default=7.5)
    minimum_tax_product_price = models.DecimalField(decimal_places=2, max_digits=12, default=2000.0)
    minimum_tax_rate_percent = models.DecimalField(decimal_places=2, max_digits=6, default=2.5)
    has_verified_bank_acct = models.BooleanField(default=False)
    role = models.CharField(max_length=100, choices=[('restaurants', 'restaurants')], default='restaurants')

    # user_role = models.ForeignKey(Roles, on_delete=models.CASCADE, null=True, blank=True)
    account_status = models.CharField(max_length=100, choices=[('active', 'active'), ('pending', 'pending'), ('deactivated', 'deactivated')], default='pending')
    is_dineqr_staff = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.generate_custom_id()
        if not self.qr_code:
            self.generate_qr_code()

        if self.tax_rate_percent > 100:
            raise ValidationError("Tax rate cannot be greater than 100%")
        
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Restaurants"

class Staff(BaseUser):
    restaurant = models.ForeignKey(Restaurant, related_name='staffs', on_delete=models.CASCADE)
    custom_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    role = models.CharField(max_length=100, choices=[('staffs', 'staffs')], default='staffs')

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.generate_custom_id()

        if not self.logo:
            self.logo = self.restaurant.logo

        if not self.qr_code:
            self.qr_code = self.restaurant.qr_code

        if not self.currency:
            self.currency = self.restaurant.currency

        if not self.restaurant_link:
            self.restaurant_link = self.restaurant.restaurant_link

        if not self.address:
            self.address = self.restaurant.address

        if not self.phone_number:
            self.phone_number = self.restaurant.phone_number

        if not self.city:
            self.city = self.restaurant.city

        if not self.state:
            self.state = self.restaurant.state

        if not self.zip_code:
            self.zip_code = self.restaurant.zip_code

        if not self.country:
            self.country = self.restaurant.country

        if not self.description:
            self.description = self.restaurant.description

        existing_staff_email = Staff.objects.filter(email=self.email, restaurant=self.restaurant).exclude(pk=self.pk)
        if existing_staff_email.exists():
            raise ValidationError('Staff with this email already exists for this restaurant.')

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Staffs"

class Customer(BaseUser):
    custom_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    role = models.CharField(max_length=100, choices=[('customers', 'customers')], default='customers')

    def save(self, *args, **kwargs):
        if not self.custom_id:
            self.generate_custom_id()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Customers"


class RestaurantsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='restaurants')

class RestaurantProxy(Restaurant):
    objects = RestaurantsManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Restaurants"

class RestaurantStaffsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='staffs')

class StaffProxy(Staff):
    objects = RestaurantStaffsManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Staffs"

class CustomersManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(role='customers')

class CustomerProxy(Customer):
    objects = CustomersManager()

    class Meta:
        proxy = True
        verbose_name_plural = "Customers"















































# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.utils.translation import gettext_lazy as _
# from django.core.validators import RegexValidator
# from django.core.files.uploadedfile import InMemoryUploadedFile
# import uuid
# import qrcode
# from io import BytesIO
# from django.core.files.base import ContentFile


# # Custom user manager for creating users and superusers
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError(_('The email must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_active', True)
#         return self.create_user(email, password, **extra_fields)

# # Abstract base user class
# class BaseUser(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(_('email address'), unique=True)
#     first_name = models.CharField(_('first name'), max_length=150, blank=True)
#     last_name = models.CharField(_('last name'), max_length=150, blank=True)
#     is_active = models.BooleanField(_('active'), default=True)
#     is_staff = models.BooleanField(_('staff status'), default=False)
#     date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
#     profile_image = models.ImageField(upload_to='users/profile_images/', blank=True, null=True)
#     is_email_verified = models.BooleanField(default=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     class Meta:
#         abstract = True

# # Restaurant model
# class Restaurant(BaseUser):
#     name = models.CharField(max_length=200, unique=True)
#     address = models.TextField()
#     phone_number = models.CharField(
#         max_length=15,
#         validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
#         blank=True,
#         null=True
#     )
#     qr_code = models.ImageField(upload_to='restaurants/qr_codes/', blank=True, null=True)

#     def save(self, *args, **kwargs):
#         if not self.qr_code:
#             self.generate_qr_code()
#         super().save(*args, **kwargs)

#     def generate_qr_code(self):
#         qr = qrcode.make(self.get_absolute_url())
#         canvas = BytesIO()
#         qr.save(canvas, format='PNG')
#         file_name = f'qr_{self.pk}.png'
#         self.qr_code.save(file_name, ContentFile(canvas.getvalue()), save=False)
#         canvas.close()

#     def get_absolute_url(self):
#         return f"https://{self.name}.myapp.com"
    
#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name=_('groups'),
#         blank=True,
#         help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
#         related_name="restaurant_groups",
#         related_query_name="restaurant",
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name=_('user permissions'),
#         blank=True,
#         help_text=_('Specific permissions for this user.'),
#         related_name="restaurant_user_permissions",
#         related_query_name="restaurant",
#     )


# # Staff model
# class Staff(BaseUser):
#     restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='staff')

#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name=_('groups'),
#         blank=True,
#         help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
#         related_name="staff_groups",
#         related_query_name="staff",
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name=_('user permissions'),
#         blank=True,
#         help_text=_('Specific permissions for this user.'),
#         related_name="staff_user_permissions",
#         related_query_name="staff",
#     )

# # Customer model
# class Customer(BaseUser):
#     phone_number = models.CharField(
#         max_length=15,
#         validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")],
#         blank=True,
#         null=True
#     )
#     birth_date = models.DateField(blank=True, null=True)
#     address = models.TextField(blank=True, null=True)
#     city = models.CharField(max_length=100, blank=True, null=True)
#     state = models.CharField(max_length=100, blank=True, null=True)
#     country = models.CharField(max_length=100, blank=True, null=True)
#     zip_code = models.CharField(max_length=12, blank=True, null=True)
#     loyalty_points = models.IntegerField(default=0)
#     preferences = models.JSONField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.email} - {self.first_name} {self.last_name}"
    
#     groups = models.ManyToManyField(
#         'auth.Group',
#         verbose_name=_('groups'),
#         blank=True,
#         help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
#         related_name="customer_groups",
#         related_query_name="customer",
#     )
#     user_permissions = models.ManyToManyField(
#         'auth.Permission',
#         verbose_name=_('user permissions'),
#         blank=True,
#         help_text=_('Specific permissions for this user.'),
#         related_name="customer_user_permissions",
#         related_query_name="customer",
#     )
