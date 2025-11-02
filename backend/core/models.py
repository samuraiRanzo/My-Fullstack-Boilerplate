from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Blog(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        DENIED = 'DENIED', _('Denied')

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blogs',
        verbose_name=_('author'),
    )
    title = models.CharField(max_length=255, verbose_name=_('title'))
    content = models.TextField(verbose_name=_('content'))
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
        verbose_name=_('status'),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
        ]
        verbose_name = _('blog')
        verbose_name_plural = _('blogs')

    def __str__(self) -> str:
        return f"{self.title} ({self.get_status_display()})"
