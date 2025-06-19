from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Favourite

@api_view(['POST'])
def add_favourite(request):
    username = request.data.get('username')
    city = request.data.get('city')

    if not username or not city:
        return Response({'error': 'Username and city are required'}, status=400)

    Favourite.objects.create(username=username, city=city)
    return Response({'message': f'City "{city}" added to favourites for user "{username}"'})

@api_view(['GET', 'POST'])
def list_favourites(request):
    username = request.query_params.get('username') if request.method == 'GET' else request.data.get('username')

    if not username:
        return Response({'error': 'Username is required'}, status=400)

    favs = Favourite.objects.filter(username=username)
    data = [{"id": fav.id, "city": fav.city} for fav in favs]
    return Response({'favourites': data})

@api_view(['POST'])
def remove_favourite(request, favourite_id):
    username = request.data.get('username')

    if not username:
        return Response({'error': 'Username is required'}, status=400)

    result = Favourite.objects.filter(id=favourite_id, username=username).delete()

    if result[0] == 1:
        return Response({'message': 'Favourite removed'})
    else:
        return Response({'error': 'Favourite not found'})
