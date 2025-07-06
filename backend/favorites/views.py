# backend/favorites/views.py
from rest_framework import generics, permissions
from .models import Favorite
from .serializers import FavoriteSerializer

class FavoriteListCreateView(generics.ListCreateAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated] # Only authenticated users can access

    def get_queryset(self):
        """
        Returns a list of all favorites for the authenticated user.
        """
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Sets the user of the favorite to the current authenticated user.
        """
        serializer.save(user=self.request.user)

class FavoriteDestroyView(generics.DestroyAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Ensures a user can only delete their own favorites.
        """
        return Favorite.objects.filter(user=self.request.user)