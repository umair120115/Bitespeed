from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required!")
        if not password:
            raise ValueError("Password is required!")

        extra_fields.setdefault("is_active", True)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable =False)
    username = models.CharField(unique=True,  max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["name", "password"]

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def has_module_perms(self, app_label):
        return True

    def has_perm(self, perm, obj=None):
        return True
    
    def all_contacts(self):
        return self.user.all()
    
class Contact(models.Model):
    PRECEDENCE = [
        ('primary','Primary'),
        ('secondary','Secondary')
    ]
    id =  models.UUIDField(primary_key=True, default = uuid.uuid4 ,editable=False)
    # user= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    phone= models.CharField( max_length=15, blank=True, null=True)
    email= models.EmailField(blank=True, null=True)
    linkedId = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='contact')
    linkPrecedence = models.CharField(max_length=255, choices=PRECEDENCE, default='primary')
    createdAt=models.DateTimeField(auto_now_add=True)
    deletedAt= models.DateTimeField(blank=True, null=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.phone if self.phone else self.email} & {self.email} "

