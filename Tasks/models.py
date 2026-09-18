from django.db import models
from django.contrib.auth.models import User

from clans.models import Clan

# Create your models here.
class ClanTask(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('doing', 'Doing'),
        ('done', 'Done'),
    ]

    clan = models.ForeignKey(Clan, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='todo')
    xp_reward = models.IntegerField(default=50)

    participants = models.ManyToManyField(User, blank=True, related_name='tasks_participating')

    deadline = models.DateField(null=True, blank=True)  # 👈 сразу упростим (см. пункт 2)

    created_at = models.DateTimeField(auto_now_add=True)



class ClanTaskCompletion(models.Model):
    task = models.ForeignKey(ClanTask, on_delete=models.CASCADE, related_name='completions')
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    completed_at = models.DateTimeField(auto_now_add=True)