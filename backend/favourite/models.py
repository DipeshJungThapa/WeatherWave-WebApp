from django.conf import settings
from django.db import models

class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.city} (user: {self.user.username})'
