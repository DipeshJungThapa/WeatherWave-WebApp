# backend/Login_Auth/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    This allows for creating users with both a username and an email.
    The username is used as the primary authentication field.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email) # Normalizes the email address (e.g., lowercasing domain part)

        # Create user instance with username and email
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password) # Hashes the password securely
        user.save(using=self._db) # Saves the user to the database
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        # Set default values for superuser specific fields
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True) # Superusers should always be active by default

        # Enforce required superuser fields
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True.')

        # Call the create_user method to create the superuser
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's default AbstractUser.
    It is configured to use 'username' as the primary authentication field
    and ensures that 'email' is also a unique and required field.
    """
    # Explicitly define username field to make it unique, non-blank, and non-nullable.
    username = models.CharField(max_length=150, unique=True, blank=False, null=False) # <--- THIS MUST BE blank=False, null=False

    # Explicitly define email field to make it unique, non-blank, and non-nullable.
    email = models.EmailField(unique=True, blank=False, null=False)

    # Assign our custom user manager to this model
    objects = CustomUserManager()

    # Define the field that will be used as the unique identifier for authentication (login).
    USERNAME_FIELD = 'username'

    # Define a list of field names that will be prompted when creating a user via
    # the `createsuperuser` command, in addition to USERNAME_FIELD (username) and password.
    REQUIRED_FIELDS = ['email'] # 'email' will be asked for when creating a superuser

    # Add a string representation for better readability in the Django admin interface
    def __str__(self):
        return self.username # Returns the username as the primary identifier for display