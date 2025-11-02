from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # Keep a username for login; make email unique and required
    email = models.EmailField(_('email address'), unique=True, blank=False, null=False)

    # Placeholders for future extension, e.g.:
    # phone = models.CharField(max_length=20, blank=True)
    # is_email_verified = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.username or self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
