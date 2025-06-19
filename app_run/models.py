from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Status(models.TextChoices):
    INIT = 'INIT', 'init'
    IN_PROGRESS = 'WIP', 'in_progress'
    FINISHED = 'DONE', 'finished'


class Run(models.Model):
    athlete = models.ForeignKey(
        user,
        on_delete=models.CASCADE,
        related_name='runs',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    status = models.CharField(
        max_length=4,
        choices=Status,
        default=Status.INIT,
    )

    class Meta:
        db_table = 'run'
        verbose_name = 'Забег'
        verbose_name_plural = 'Забеги'
