from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Favourite

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favourite(request):
    city = request.data.get('city')
    if not city:
        return Response({'error': 'City is required'}, status=400)
    Favourite.objects.create(user=request.user, city=city)
    return Response({'message': f'City "{city}" added to favourites for user "{request.user.email}"'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favourites(request):
    favs = Favourite.objects.filter(user=request.user)
    data = [{"id": fav.id, "city": fav.city} for fav in favs]
    return Response({'favourites': data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_favourite(request, favourite_id):
    result = Favourite.objects.filter(id=favourite_id, user=request.user).delete()
    if result[0] == 1:
        return Response({'message': 'Favourite removed'})
    else:
        return Response({'error': 'Favourite not found'})