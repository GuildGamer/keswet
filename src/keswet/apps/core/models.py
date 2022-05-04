from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import NewBaseUserManager
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    id = models.BigAutoField(primary_key=True, unique=True, db_index=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    phone = models.CharField("Phone Number", max_length=40, blank=True, null=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    token = models.TextField(blank=True, null=True)

    objects = NewBaseUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    first_name = models.CharField("First Name", max_length=100, blank=True)
    last_name = models.CharField("Last Name", max_length=100, blank=True)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)
