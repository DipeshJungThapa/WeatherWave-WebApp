from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status # Crucial Change 1: Import status for clear HTTP responses
from .models import Favourite
from .serializers import FavouriteSerializer # Crucial Change 2: Import the new FavouriteSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favourite(request):
    # Crucial Change 3: Expect 'district' from frontend payload, map to 'district_name' for model
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
    # Crucial Change 4: Use the serializer to return consistent and structured favorite data
    serializer = FavouriteSerializer(favourite)
    return Response(
        {"message": f"District '{district_name}' added to favorites for user '{request.user.username}'",
         "favourite": serializer.data},
        status=status.HTTP_201_CREATED # 201 Created for successful resource creation
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favourites(request):
    favs = Favourite.objects.filter(user=request.user)
    # Crucial Change 5: Use the serializer for listing favorites
    serializer = FavouriteSerializer(favs, many=True)
    return Response({'favourites': serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST']) # Using POST for removal as it changes state, can also be DELETE with different URL pattern
@permission_classes([IsAuthenticated])
def remove_favourite(request):
    # Crucial Change 6: Expect 'district' in request body for removal, consistent with add
    district_name = request.data.get('district')
    if not district_name:
        return Response({'error': 'District name is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Crucial Change 7: Filter by user and district_name to find the favorite to remove
        favourite = Favourite.objects.get(user=request.user, district_name=district_name)
        favourite.delete()
        return Response(
            {"message": f"District '{district_name}' removed from favorites."},
            status=status.HTTP_200_OK
        )
    except Favourite.DoesNotExist:
        return Response(
            {"error": "Favourite not found for this user and district"},
            status=status.HTTP_404_NOT_FOUND # 404 if the specific favorite doesn't exist to remove
        )