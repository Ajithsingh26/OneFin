from rest_framework import serializers
from django.contrib.auth.models import User
import re
from .models import Collection, Movie

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
        error_messages={
            'min_length': "Password must be at least 8 characters long.",
            'max_length': "Password cannot exceed 128 characters."
        }
    )
    username = serializers.CharField(
        max_length=150,
        error_messages={
            'max_length': "Username cannot exceed 150 characters."
        }
    )

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        if not re.match(r'^[a-zA-Z0-9_]+$', value):
            raise serializers.ValidationError(
                "Username can only contain letters, numbers, and underscores."
            )
        return value

    def validate_password(self, value):
        password_requirements = [
            (r'[A-Z]', "Password must contain at least one uppercase letter."),
            (r'[a-z]', "Password must contain at least one lowercase letter."),
            (r'[0-9]', "Password must contain at least one digit."),
            (r'[!@#$%^&*(),.?":{}|<>]', "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")
        ]

        for pattern, message in password_requirements:
            if not re.search(pattern, value):
                raise serializers.ValidationError(message)

        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class MovieSerializer(serializers.ModelSerializer):
    uuid = serializers.CharField()
    
    class Meta:
        model = Movie
        fields = ['uuid', 'title', 'description', 'genres']

class CollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, required=False)

    class Meta:
        model = Collection
        fields = ['uuid', 'title', 'description', 'movies']

    def validate(self, attrs):
        user = self.context['request'].user
        title = attrs.get('title')

        if self.context['request'].method == 'POST':
            if Collection.objects.filter(user=user, title=title).exists():
                raise serializers.ValidationError({'title': 'A collection with this title already exists.'})

        return attrs

    def create(self, validated_data):
        movies_data = validated_data.pop('movies', [])
        
        collection = Collection.objects.create(**validated_data)

        new_movies_data = []

        if not movies_data:
            response_message = {
                'collection_uuid': collection.uuid,
            }
            return collection, response_message

        for movie_data in movies_data:
            movie, _ = Movie.objects.get_or_create(
                uuid=movie_data['uuid'],
                defaults={'title': movie_data['title'], 'description': movie_data['description'], 'genres': movie_data['genres']}
            )

            new_movies_data.append(movie.title)

        response_message = {
            'collection_uuid': collection.uuid,
            'message': 'Collection created with some new movies.',
            'new_movies_added': new_movies_data
        }
        

        return collection, response_message

    def update(self, instance, validated_data):
        movies_data = validated_data.pop('movies', [])

        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        already_added_movies = []
        new_movies_added = []

        if movies_data:
            request_method = self.context['request'].method

            if request_method == 'PUT':
                instance.movies.clear()

            for movie_data in movies_data:
                movie, _ = Movie.objects.get_or_create(
                    uuid=movie_data['uuid'],
                    defaults={'title': movie_data['title'], 'description': movie_data['description'], 'genres': movie_data['genres']}
                )
                if instance.movies.filter(uuid=movie.uuid).exists():
                    already_added_movies.append(movie.title)
                else:
                    instance.movies.add(movie)
                    new_movies_added.append(movie.title)

            response_message = {
                'collection_uuid': instance.uuid,
                'message': 'Collection updated successfully.',
                'new_movies_added': new_movies_added
            }

            if request_method == 'PATCH':
                response_message['already_added_movies'] = already_added_movies

            return instance, response_message

        return instance, {'collection_uuid': instance.uuid, 'message': 'Collection updated successfully.'}
