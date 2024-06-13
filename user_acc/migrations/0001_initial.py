# Generated by Django 5.0 on 2024-06-13 22:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('country', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Otp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.PositiveIntegerField(unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=2500, null=True)),
                ('last_name', models.CharField(blank=True, max_length=2500, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=2000, null=True)),
                ('state', models.CharField(blank=True, max_length=2000, null=True)),
                ('country', models.CharField(blank=True, max_length=2000, null=True)),
                ('zip_code', models.PositiveBigIntegerField(blank=True, null=True)),
                ('profile_image', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_phonenumber_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=2000, unique=True)),
                ('restaurant_owner', models.CharField(max_length=2000)),
                ('description', models.TextField(blank=True, null=True)),
                ('banner_image', models.TextField(blank=True, null=True)),
                ('image_one', models.TextField(blank=True, null=True)),
                ('image_two', models.TextField(blank=True, null=True)),
                ('image_three', models.TextField(blank=True, null=True)),
                ('logo', models.TextField(blank=True, null=True)),
                ('opening_hour', models.DateTimeField(blank=True, null=True)),
                ('closing_hour', models.DateTimeField(blank=True, null=True)),
                ('custom_id', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='restaurants/qr_codes/')),
                ('restaurant_link', models.TextField(blank=True, null=True)),
                ('next_subscription_date', models.DateField(blank=True, null=True)),
                ('paystack_recipient_code', models.TextField(blank=True, null=True)),
                ('tax_rate_percent', models.DecimalField(decimal_places=2, default=7.5, max_digits=6)),
                ('minimum_tax_product_price', models.DecimalField(decimal_places=2, default=2000.0, max_digits=12)),
                ('minimum_tax_rate_percent', models.DecimalField(decimal_places=2, default=2.5, max_digits=6)),
                ('has_verified_bank_acct', models.BooleanField(default=False)),
                ('role', models.CharField(choices=[('restaurants', 'restaurants')], default='restaurants', max_length=100)),
                ('account_status', models.CharField(choices=[('active', 'active'), ('pending', 'pending'), ('deactivated', 'deactivated')], default='pending', max_length=100)),
                ('is_dineqr_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, related_name='%(class)s_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='%(class)s_set', to='auth.permission')),
            ],
            options={
                'verbose_name_plural': 'Restaurants',
            },
        ),
        migrations.CreateModel(
            name='RestaurantProxy',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Restaurants',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user_acc.restaurant',),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=2500, null=True)),
                ('last_name', models.CharField(blank=True, max_length=2500, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=2000, null=True)),
                ('state', models.CharField(blank=True, max_length=2000, null=True)),
                ('country', models.CharField(blank=True, max_length=2000, null=True)),
                ('zip_code', models.PositiveBigIntegerField(blank=True, null=True)),
                ('profile_image', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_phonenumber_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('custom_id', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('role', models.CharField(choices=[('customers', 'customers')], default='customers', max_length=100)),
                ('groups', models.ManyToManyField(blank=True, related_name='%(class)s_set', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='%(class)s_set', to='auth.permission')),
            ],
            options={
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='CustomerProxy',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Customers',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user_acc.customer',),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=2500, null=True)),
                ('last_name', models.CharField(blank=True, max_length=2500, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('city', models.CharField(blank=True, max_length=2000, null=True)),
                ('state', models.CharField(blank=True, max_length=2000, null=True)),
                ('country', models.CharField(blank=True, max_length=2000, null=True)),
                ('zip_code', models.PositiveBigIntegerField(blank=True, null=True)),
                ('profile_image', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('is_email_verified', models.BooleanField(default=False)),
                ('is_phonenumber_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('custom_id', models.CharField(blank=True, max_length=10, null=True, unique=True)),
                ('role', models.CharField(choices=[('staffs', 'staffs')], default='staffs', max_length=100)),
                ('groups', models.ManyToManyField(blank=True, related_name='%(class)s_set', to='auth.group')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staffs', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='%(class)s_set', to='auth.permission')),
            ],
            options={
                'verbose_name_plural': 'Staffs',
            },
        ),
        migrations.CreateModel(
            name='StaffProxy',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Staffs',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user_acc.staff',),
        ),
    ]
