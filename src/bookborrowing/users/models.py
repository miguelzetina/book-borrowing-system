from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.db import models
from django.utils.translation import ugettext_lazy as _

from bookborrowing.core.db.models import CatalogueMixin, TimeStampedMixin


class Role(CatalogueMixin):
    """
    Model for User role
    """
    description = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = _('role')
        verbose_name_plural = _('roles')

    def __str__(self):
        return "{}: {}".format(self.name, self.description)


class UserManager(BaseUserManager):
    """
    Custom manager for create superusers.
    """

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create new user superuser.
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        role, created = Role.objects.get_or_create(name='superadmin')
        extra_fields.setdefault(
            'role_id', role.id
        )
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, CatalogueMixin):
    """
    Custom user model yo be used accross the app.
    """
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name=_('email')
    )

    last_name = models.CharField(
        max_length=255,
        verbose_name=_('last name')
    )

    second_last_name = models.CharField(
        max_length=255,
        verbose_name=_('second last name')
    )

    role = models.ForeignKey(
        Role,
        related_name='users',
        related_query_name='user',
        on_delete=models.CASCADE
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('is staff')
    )

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    class JSONAPIMeta:
        resource_name = 'users'

    def __str__(self):
        return " ".join([self.name, self.last_name, self.second_last_name])

    @property
    def has_admin_permissions(self):
        return self.role.name == 'admin'

    @property
    def has_superadmin_permissions(self):
        return self.role.name == 'superadmin'