from distutils.command.upload import upload
# A new class is imported. ##
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import random
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
# from pytz import timezone
from django.utils import timezone


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """User model."""

    username = models.CharField(max_length=26)
    dob=models.CharField(max_length=100,null=True,blank=True,default="---")
    gender=models.CharField(max_length=100,blank=True,default="---")
    profile_pic = models.IntegerField(null=True)
    email = models.EmailField(_('email address'), unique=True)
    email_verified = models.BooleanField(default=False)    
    otp = models.CharField(max_length=4, blank=True, null=True)
    otp_generated_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count=models.IntegerField(null=True,default=0)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def generateotp(self):
        otp = random.randint(1000, 9999)
        self.otp_generated_at = timezone.now()
        self.otp = str(otp)
        self.save()

    def verifyotp(self):
        self.email_verified = True
        self.otp = None
        self.save()
