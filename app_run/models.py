from django.contrib.auth import get_user_model
from django.db import models


user = get_user_model()


class Run(models.Model):
    athlete = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='runs',
    )
    created_at = models.DateTimeField(auto_now=True)
    comment = models.TextField()

    class Meta:
        db_table = 'run'
        verbose_name = 'Забег'
        verbose_name_plural = 'Забеги'
