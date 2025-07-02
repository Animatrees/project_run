from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Status(models.TextChoices):
    INIT = 'init', 'init'
    IN_PROGRESS = 'in_progress', 'in_progress'
    FINISHED = 'finished', 'finished'


class Run(models.Model):
    athlete = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='runs',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    status = models.CharField(
        max_length=15,
        choices=Status,
        default=Status.INIT,
    )

    class Meta:
        db_table = 'run'
        verbose_name = 'Забег'
        verbose_name_plural = 'Забеги'


class AthleteInfo(models.Model):

    weight = models.IntegerField(
        null=True,
        blank=True,
    )
    goals = models.TextField(blank=True, default='')
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
