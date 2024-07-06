"""
Database models.
"""


from django.db import models
from django.contrib.auth.modles import (
    AbstartBaseUser,
    BaseUserManger,
    PermissionsMixin,
)
class UserManager(BaseUserManger):
    """Manager for users."""

    def create_user(self,email, password=None, **extra_field):
        """Create, save and return a new user."""
        user = self.model(email=email, **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

class User(AbstartBaseUser,PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique = True)
    name= models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(deafult=False)

    USERNAME_FIELD = 'email'
