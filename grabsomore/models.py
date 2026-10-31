"""Database models for password reset tokens and account recovery."""

from django.conf import settings
from django.db import models


class ResetToken(models.Model):
    """Ephemeral, single-use authentication token for password recovery."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    token = models.CharField(max_length=255)
    expiry_date = models.DateTimeField()
    used = models.BooleanField(default=False)

    def __str__(self):
        """Return reset token user reference."""
        return f"ResetToken for {self.user.username}"
