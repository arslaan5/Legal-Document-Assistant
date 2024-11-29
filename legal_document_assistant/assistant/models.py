from django.db import models
from uuid import uuid4
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Custom User Manager
class UserInfoManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username must be set")
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)


# Custom User Model
class UserInfo(AbstractBaseUser, PermissionsMixin):
    user_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    username = models.CharField(max_length=20, unique=True, blank=False)
    email = models.EmailField(max_length=100, unique=True, blank=False)
    password = models.CharField(max_length=100, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access
    is_superuser = models.BooleanField(default=False)

    objects = UserInfoManager()

    USERNAME_FIELD = 'username'  # Unique field for authentication
    REQUIRED_FIELDS = ['email']  # Required fields when creating a superuser

    def __str__(self):
        return self.username
