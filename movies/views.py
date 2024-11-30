from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Collection
from .serializers import RegisterSerializer, CollectionSerializer, MovieSerializer
from django.conf import settings
from django.core.cache import cache
from .utils import MovieAPIClient
from collections import Counter
import redis

class RequestCountView(APIView):
    def get(self, request):
        redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
        request_count = redis_client.get('request_count')
        
        if not request_count:
            request_count = 0
        
        return Response({'requests': int(request_count)}, status=status.HTTP_200_OK)

class ResetRequestCountView(APIView):
    def post(self, request):
        redis_client = redis.StrictRedis.from_url(settings.CACHES['default']['LOCATION'])
        redis_client.set('request_count', 0)
        
        return Response({'message': 'Request count reset successfully'}, status=status.HTTP_200_OK)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MovieListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = int(request.query_params.get('page', 1))

        cache_key = f"movies_list_page_{page}"
        cached_movies = cache.get(cache_key)
        if cached_movies:
            return Response({"movies": cached_movies}, status=status.HTTP_200_OK)

        api_client = MovieAPIClient()
        url = settings.EXTERNAL_MOVIES_API_URL
        auth = (settings.API_USERNAME, settings.API_PASSWORD)

        result = api_client.fetch_movies(url, auth, page)

        if "error" in result:
            return Response({"error": "Failed to fetch movies", "details": result["error"]}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        movie_data = result.get("results", [])
        movies = [MovieSerializer(movie).data for movie in movie_data]
        total_count = result.get("count", 0)

        cache.set(cache_key, movies, timeout=3600)

        return Response({"count": total_count, "page": page, "movies": movies}, status=status.HTTP_200_OK)

class CollectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all()
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            _, response_message = serializer.save(user=request.user)
            return Response(response_message, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        collections = self.get_queryset()
        serializer = self.get_serializer(collections, many=True)

        genres_count = Counter()
        for collection in collections:
            for movie in collection.movies.all():
                genres_count.update(genre.strip() for genre in movie.genres.split(','))

        sorted_genres = sorted(genres_count.items(), key=lambda x: x[1], reverse=True)[:3]
        favorite_genres = ', '.join([genre for genre, _ in sorted_genres])

        return Response({
            'is_success': True,
            'data': {
                'collections': serializer.data,
                'favourite_genres': favorite_genres
            }
        })

    def retrieve(self, request, *args, **kwargs):
        collection = self.get_object()
        serializer = self.get_serializer(collection)
        response_data = {
            'title': collection.title,
            'description': collection.description,
            'movies': serializer.data.get('movies', [])
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        collection = self.get_object()
        serializer = self.get_serializer(collection, data=request.data, partial=partial)

        if serializer.is_valid():
            _, response_message = serializer.save()
            return Response(response_message, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        collection = self.get_object()
        collection_uuid = collection.uuid
        collection.delete()
        return Response(
            {'message': f'Collection with UUID {collection_uuid} has been deleted.'},
            status=status.HTTP_204_NO_CONTENT
        )
