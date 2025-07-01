# backend/favourite/views.py

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Favourite
from .serializers import FavouriteSerializer # Make sure this is correctly imported

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favourite(request):
    """
    Adds a district to the user's favorites.
    Requires authentication.
    """
    district_name = request.data.get('district')

    if not district_name:
        return Response({'error': 'District name is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if favorite already exists for this user and district
    if Favourite.objects.filter(user=request.user, district_name=district_name).exists():
        return Response(
            {"message": f"District '{district_name}' is already in your favorites."},
            status=status.HTTP_200_OK # 200 OK because it's not an error, just already exists
        )

    # Create the favorite
    favourite = Favourite.objects.create(user=request.user, district_name=district_name)
    serializer = FavouriteSerializer(favourite) # Use the serializer to return consistent data
    return Response(
        {"message": f"District '{district_name}' added to favorites for user '{request.user.username}'",
         "favourite": serializer.data},
        status=status.HTTP_201_CREATED # 201 Created for successful resource creation
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favourites(request):
    """
    Lists all favorite districts for the authenticated user.
    Requires authentication.
    """
    favs = Favourite.objects.filter(user=request.user)
    serializer = FavouriteSerializer(favs, many=True) # Use the serializer for listing favorites
    return Response({'favourites': serializer.data}, status=status.HTTP_200_OK)

@api_view(['DELETE']) # This is the ONLY remove_favourite function, handling DELETE requests
@permission_classes([IsAuthenticated])
def remove_favourite(request):
    """
    Removes a district from the user's favorites.
    Requires authentication.
    Expects 'district' in the request body for DELETE method.
    """
    district_name = request.data.get('district') # For DELETE, request.data is used for body content
    if not district_name:
        return Response({'error': 'District name is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Filter by user and district_name to find the specific favorite to remove
        favourite = Favourite.objects.get(user=request.user, district_name=district_name)
        favourite.delete()
        return Response(
            {"message": f"District '{district_name}' removed from favorites."},
            status=status.HTTP_200_OK # 200 OK for successful deletion
        )
    except Favourite.DoesNotExist:
        return Response(
            {"error": "Favourite not found for this user and district"},
            status=status.HTTP_404_NOT_FOUND # 404 if the specific favorite doesn't exist to remove
        )