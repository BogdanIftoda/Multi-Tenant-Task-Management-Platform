from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from tenant.base_model import BaseModel


class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Role(models.Model):
    USER = "U"
    ADMIN = "A"
    SUPERUSER = "S"

    ROLES = {
        USER: "user",
        ADMIN: "admin",
        SUPERUSER: "superuser",
    }

    name = models.CharField(max_length=1, choices=ROLES, default=USER, unique=True)

    def __str__(self):
        return self.name


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not username:
            raise ValueError("The Username field must be set")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        role, _ = Role.objects.get_or_create(name=Role.SUPERUSER)
        extra_fields.setdefault('role', role)
        return self.create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser, BaseModel):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    objects = UserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['first_name', "last_name", 'organization'],
                                    name='user: first name last name and organization constraint'),
        ]

    def __str__(self):
        return self.username

    @property
    def is_superuser(self):
        return self.role.name == Role.SUPERUSER

    @property
    def is_admin(self):
        return self.role.name == Role.ADMIN
