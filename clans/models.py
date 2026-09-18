from django.db import models
from django.contrib.auth.models import User
import random
import string

class Clan(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_clans')
    members = models.ManyToManyField(User, related_name='clans', blank=True)
    code = models.CharField(max_length=10, unique=True, blank=True)

    def generate_code(self):
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            if not Clan.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name