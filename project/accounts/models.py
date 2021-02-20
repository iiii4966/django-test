from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.forms import model_to_dict
from django.utils.functional import cached_property


class UserQuerySet(models.QuerySet):
    pass


class UserDefaultManager(BaseUserManager.from_queryset(UserQuerySet)):

    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=255, unique=True)

    objects = UserDefaultManager()

    USERNAME_FIELD = 'username'

    class Meta:
        db_table = 'auth_user'

    def is_owner(self, entry):
        if not hasattr(entry, 'user_id'):
            raise TypeError('entry must have a user_id as a property')
        return self.id == entry.user_id

    @cached_property
    def to_dict(self):
        return model_to_dict(self, fields=['id', 'username', ] )
