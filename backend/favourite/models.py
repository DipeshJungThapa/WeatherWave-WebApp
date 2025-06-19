

from django.db import models

class Favourite(models.Model):
    username = models.CharField(max_length=150)   # store as text, NOT ForeignKey
    city = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.city} (user: {self.username})'
