from cgi import print_exception
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
# Create your models here.


class Inventory(models.Model):
    title= models.CharField(max_length=30)
    description= models.CharField(max_length=30)
    price= models.IntegerField()
    quantity= models.IntegerField()
    sku= models.CharField(max_length=10)



class CustomUserManager(BaseUserManager):
    def create_superuser(self, username, email, password=None, **extra_fields):
        # Create and return a superuser with the given fields
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Additional fields specific to your custom user model
    # ...

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    # Define related_name for groups and user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='custom_users'  # Change 'custom_users' to your desired related_name
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='custom_users_permissions'  # Change 'custom_users_permissions' to your desired related_name
    )

    # ...

    def __str__(self):
        return self.username
