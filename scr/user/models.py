from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
import jwt
import re


def validate_password(value):
    if len(value) < 10:
        raise ValidationError('The given password must have 10 characters or more')

    regex_uppercase = "^(?=.*[A-Z]).+$"
    regex_value = re.compile(regex_uppercase)
    if not re.search(regex_value, value):
        raise ValidationError('Validate the password value contains at least one uppercase letter')

    regex_lowercase = "^(?=.*[a-z]).+$"
    regex_value = re.compile(regex_lowercase)
    if not re.search(regex_value, value):
        raise ValidationError('Validate the password value contains at least one lowercase letter')

    regex_special_character = "^(?=.*[\]!@#?]).+$"
    regex_value = re.compile(regex_special_character)
    if not re.search(regex_value, value):
        raise ValidationError('Validate the password value contains at least one ' +
                              'of the following characters: !, @, #, ? or ]')


class CustomUserManager(UserManager):
    def _create_user(self, email, password, username=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValidationError("The given email must be set")

        validate_password(password)
        email = self.normalize_email(email)
        user = self.model(username=email, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    """
    Custom user model
    """
    email = models.EmailField(_('email address'), blank=False, unique=True)
    password = models.CharField(_('password'), max_length=128, blank=False)

    email_verified = models.BooleanField(_("email_verified"), default=False, help_text=_(
            "True when user email is verified."
        ),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = [""]

    @property
    def token(self):
        expiration = (datetime.utcnow() + timedelta(minutes=20)).strftime('%Y-%m-%dT%H:%M:%S')
        claims = {
            'email': self.email,
            'expiration': expiration
        }
        token = jwt.encode(claims, settings.SECRET_KEY, algorithm="HS256")
        return token
