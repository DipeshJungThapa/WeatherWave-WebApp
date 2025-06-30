# backend/favourite/models.py
from django.conf import settings
from django.db import models

class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Crucial Change: Renamed 'city' to 'district_name' to match frontend payload and views
    district_name = models.CharField(max_length=100)

    # Adding Meta class for unique_together and ordering (good practice)
    class Meta:
        unique_together = ('user', 'district_name') # A user can favorite a district only once
        ordering = ['-added_at'] # Order by most recent first (requires 'added_at' field)

    def __str__(self):
        # Updated to reflect district_name
        return f'{self.district_name} (user: {self.user.username})'

# Optional: Add 'added_at' field if you want to use it for ordering and tracking
# If you add 'added_at', make sure to run makemigrations/migrate again.
# For simplicity, if you want to avoid extra migration right now, you can omit the 'added_at' field
# and the 'ordering' in Meta, but it's good practice.
# Let's add it for robustness, it's a minor migration.
    added_at = models.DateTimeField(auto_now_add=True)